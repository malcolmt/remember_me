import bisect
import random

from django.conf import settings
from django.core.cache import cache

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
    pks = word_keys(language, level)
    sampled_words = list(Word.objects.filter(pk__in=random.sample(pks,
            num_choices)))
    question_attribute, answer_attribute = random.choice(QUESTION_SCENARIOS)
    question = random.choice(sampled_words)
    question_data = (question.pk, getattr(question, question_attribute))
    answers = [(item.pk, getattr(item, answer_attribute)) 
            for item in sampled_words]
    return question_data, answers

def word_keys(code, level):
    """
    Retrieves all the pk values for words for the language "code" and "level".
    This interacts sensibly with the cache system to avoid unnecessary database
    round trips.

    Returns a list of pk values.
    """
    full_list = cache.get(code)
    if not full_list:
        full_list = tuple(Word.objects.filter(lang_code__code=code). \
                values_list("level", "pk").order_by("level"))
        cache.set(code, full_list, settings.LANG_CACHE_TIMEOUT)
    start = bisect.bisect_right(full_list, (level - 1, 0))
    end = bisect.bisect_left(full_list, (level + 1, 0))
    return [item[1] for item in full_list[start : end]]

