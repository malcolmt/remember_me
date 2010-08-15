import random

from django.conf import settings
from minerva.models import Word

QUESTION_SCENARIOS = (
    # Question, answer
    ('word', 'meaning'),
    ('meaning', 'word'),
)

def create_question(user, language, level, num_choices=4):
    """
    Returns a question and multiple plausible answers, given the user, their
    preferred language and targeted skill level.

    The returned data structure is a nested pair:
        (
            [question id, question string],
            [(answer id, answer string), ...]
        )
    """
    # TODO: Right now, this is very simple (doesn't take into account the
    # user's performance at all). Eventually, it will be a graded selection
    # based on what the user finds difficult, etc.

    # FIXME: Cache this, for each language.
    pks = Word.objects.filter(language=language, level=level). \
            values_list("pk", flat=True)
    sampled_words = list(Word.objects.filter(pk__in=random.sample(pks,
            num_choices)))
    question_attribute, answer_attribute = random.choice(QUESTION_SCENARIOS)
    question = random.choice(sampled_words)
    question_data = (question.pk, getattr(question, question_attribute))
    answers = [(item.pk, getattr(item, answer_attribute)) for item in sampled_words]

    return question_data, answers
