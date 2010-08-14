from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

class Command(BaseCommand):
    help = "Imports simplified chinese from the simplified chinese character file"
    args = '[file name]'

    def handle(self, addrport='', *args, **options):
        pass
