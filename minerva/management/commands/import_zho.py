import csv
import os
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from minerva.models import Word

FIELD_NAMES = (
    "level_id",
    "id",
    "traditional_character",
    "simplified_character",
    "pinyin",
    "english",
    "element_of_speech"
)
LANGUAGE = "zho"

class Command(BaseCommand):
    help = "Imports simplified chinese from the simplified chinese character file"
    args = '[relative file name]'

    def handle(self, filename='', *args, **options):
        
        existing = set(Word.objects.filter(language="zho").values_list("word", flat=True))
        if args or not filename:
            raise CommandError('Usage is cz %s' % self.args)
        os.path.join(os.getcwd(), filename)
        print "File path: %s" % filename
        if not os.path.exists(filename):
            raise CommandError("%s is not a valid file" % filename)
        reader = csv.DictReader(open(filename), FIELD_NAMES)
        for entry in reader:
            if entry["simplified_character"].decode("utf-8") in existing:
                # Avoiding importing the same character twice
                continue
            item = Word.objects.create(
                word=entry["simplified_character"],
                meaning=entry["english"],
                level=entry["level_id"],
                language=LANGUAGE,
            )
