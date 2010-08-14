from django.contrib.auth import models as auth_models
from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=50)
    meaning = models.TextField()
    level = models.PositiveIntegerField()
    language = models.CharField(max_length=3)

    class Meta:
        unique_together = ("word", "language")

    def __unicode__(self):
        return u"%s (%s)" % (self.word, self.meaning)


class Progress(models.Model):
    """
    Tracking historical progress for a particular user on a word.
    """
    student = models.ForeignKey(auth_models.User)
    word = models.ForeignKey(Word)
    correct = models.IntegerField(default=0)
    attempts = models.PositiveIntegerField()

    def __unicode__(self):
        return u"%s: %s => %d / %d" % (self.person, self.word, self.correct,
                self.attempts)

