"""
Import the standard Japanese vocabulary list.
"""

import os
from optparse import make_option

from django.core.management import base
from BeautifulSoup import BeautifulSoup

from minerva import models

LANG_CODE = "jpn"

class Command(base.BaseCommand):
    help = "Import Japanese vocabulary list"
    args = "[filename]"
    option_list = base.BaseCommand.option_list + (
        make_option("--strokes", action="store_true", dest="strokes",
            default=False,
            help="Import stroke count as sub-level in Word model."),
    )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise base.CommandError("Usage is import_jpn %s" % self.args)

        verbosity = int(options.get("verbosity", 0))
        strokes = options.get("strokes", False)
        source_file = os.path.join(os.getcwd(), args[0])
        soup = BeautifulSoup(open(source_file).read())
        old_data = models.Word.objects.filter(language=LANG_CODE). \
                values_list("word", "level", "sub_level", "id")
        existing = dict([(elt[0], elt[1:]) for elt in old_data])
        for row in soup.findAll("tr"):
            pos = row.td.findNextSiblings("td")
            word = pos[0].string.strip()
            strokes = int(pos[3].string)
            level = pos[4].string.strip()
            if level == "S":
                level = 7
            else:
                level = int(level)
            data = existing.get(word)
            if data:
                if data[0] == level and data[1] == strokes:
                    continue
                else:
                    pk = data[2]
            else:
                pk = None
            meaning = pos[5].string.strip()
            models.Word(id=pk, word=word, level=level, sub_level=strokes,
                    meaning=meaning, language=LANG_CODE).save()

