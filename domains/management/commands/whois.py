# -.- encoding: utf-8 -.-

import itertools
import pythonwhois
from django.core.management.base import BaseCommand
from domains.models import Domain


class Command(BaseCommand):
    """
    cartesian product (equivalent to a nested for-loop)
    of two lists of words, joined together to form a
    domain name to query whois service and store results.
    """
    help = 'Query whois for domains produced as result of cartesian product of two lists of words'
    args = '<list1 list2>'

    def query_domain_list(self, domain_list):
        for item in itertools.product(*domain_list):
            domain = "%s.com" % ''.join(item)
            self.stdout.write('%s' % (domain))
            try:
                Domain.objects.get(name__iexact=domain)
            except Domain.DoesNotExist:
                try:
                    obj = pythonwhois.get_whois(domain)
                except UnicodeDecodeError:
                    continue
                except:
                    self.stdout.write('Socket error maybe...?')
                    continue
                # available = True if not obj['contacts']['admin'] else False
                available = True if ('status' not in obj or obj['status'][0] == 'pendingDelete') else False
                self.stdout.write('%s: %s' % (domain, 'NOT AVAILABLE' if not available else 'OK******************************'))
                obj, created = Domain.objects.get_or_create(name=domain, available=available)

    def handle(self, *args, **options):
        list1, list2 = args
        fd1 = open(list1)
        fd2 = open(list2)
        list1 = [item.strip() for item in fd1.readlines()]
        list2 = [item.strip() for item in fd2.readlines()]

        # Combine items from two lists 
        list3 = [list2, list1]
        self.query_domain_list(list3)
        list3 = [list1, list2]
        self.query_domain_list(list3)

        # Combine items from same list
        list3 = [list1, list1]
        self.query_domain_list(list3)
        list3 = [list2, list2]
        self.query_domain_list(list3)
