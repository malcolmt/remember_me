"""
Import the standard Japanese vocabulary list.
"""

import os

from django.core.management import base
from BeautifulSoup import BeautifulSoup

from minerva import models

LANG_CODE = "jpn"

class Command(base.BaseCommand):
    help = "Import Japanese vocabulary list"
    args = "[filename]"

    def handle(self, *args, **options):
        if len(args) != 1:
            raise base.CommandError("Usage is import_jpn %s" % self.args)

        verbosity = int(options.get("verbosity", 0))
        source_file = os.path.join(os.getcwd(), args[0])
        soup = BeautifulSoup(open(source_file).read())
        existing = set(models.Word.objects.filter(language=LANG_CODE). \
                values_list("word", flat=True))
        for row in soup.findAll("tr"):
            pos = row.td.findNextSiblings("td")
            word = pos[0].string.strip()
            if word in existing:
                continue
            level = pos[4].string.strip()
            if level == "S":
                level = 7
            else:
                level = int(level)
            meaning = pos[5].string.strip()
            models.Word(word=word, level=level, meaning=meaning,
                    language=LANG_CODE).save()

