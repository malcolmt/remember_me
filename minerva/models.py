from django.contrib.auth import models as a_models
from django.contrib.sessions import models as s_models
from django.db import models

# pylint: disable-msg=E1101,W0232

class WordManager(models.Manager):
    def get_by_natural_key(self, word, language):
        return self.get(word=word, language=language)

class Word(models.Model):
    """
    A logical word in a language that can be used in questions
    """
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
    anon_student = models.CharField(max_length=32, null=True, blank=True,
            help_text="Anonymous user progress is tracked using their session key.")
    word = models.ForeignKey(Word)
    correct = models.IntegerField(default=0)
    attempts = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "progress"

    def __unicode__(self):
        return u"%s: %s => %s / %d" % (self.student_string(), self.word,
                self.correct, self.attempts)

    def is_anonymous(self):
        return self.anon_student is not None

    def student_string(self):
        if self.is_anonymous():
            return u"Anon: %s" % self.anon_student
        else:
            return unicode(self.student)
    student_string.short_description = "student"

class UserProfile(models.Model):
    """
    Tracking user specific settings
    """
    student = models.ForeignKey(a_models.User, null=False, blank=False, primary_key=True)
    language = models.CharField(max_length=3)

    def __unicode__(self):
        return u"%s (%s)" % (unicode(self.student), self.language)
