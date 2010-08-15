from django.contrib.auth import models as a_models
from django.contrib.sessions import models as s_models
from django.db import models

# pylint: disable-msg=E1101,W0232

class WordManager(models.Manager):
    def get_by_natural_key(self, word, language):
        return self.get(word=word, language=language)

class Word(models.Model):
    word = models.CharField(max_length=50)
    meaning = models.TextField()
    level = models.PositiveIntegerField()
    sub_level = models.PositiveIntegerField(blank=True, null=True)
    language = models.CharField(max_length=3)

    objects = WordManager()

    class Meta:
        unique_together = ("word", "language")

    def __unicode__(self):
        return u"%s (%s)" % (self.word, self.meaning)

    def natural_key(self):
        return (self.word, self.language)


class Progress(models.Model):
    """
    Tracking historical progress for a particular user on a word.
    """
    student = models.ForeignKey(a_models.User, null=True, blank=True)
    anon_student = models.ForeignKey(s_models.Session, null=True, blank=True,
            help_text="Anonymous user progress is tracked using their session.")
    word = models.ForeignKey(Word)
    correct = models.IntegerField(default=0)
    attempts = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "progress"

    def __unicode__(self):
        return u"%s,%s: %s => %d / %d" % (self.student, self.anon_student, self.word, self.correct,
                self.attempts)

    def is_anonymous(self):
        return self.anon_student is not None

