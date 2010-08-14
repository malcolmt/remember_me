import random

from minerva.models import Word

QUESTION_SCENARIOS = (
    # Question, answer
    ('word', 'meaning'),
    ('meaning', 'word'),

)

def create_question(user, language, level):
    """
    Returns a question and multiple plausible answers, given the user, their
    preferred language and targeted skill level.

    Right now, this is very simple (doesn't take into account the user's
    performance at all). Eventually, it will be a graded selection based on
    what the user finds difficult, etc.
    """
    # FIXME - maybe sanity check language
    # FIXME: Cache this, for each language.
    pks = Word.objects.filter(language=language, level=level).values_list("pk", flat=True)
    sampled_words = Word.objects.filter(pk__in=random.sample(pks, 4))
    question_attribute, answer_attribute = random.choice(QUESTION_SCENARIOS)
    question = getattr(sampled_words[0], question_attribute)
    answers = [getattr(item, answer_attribute) for item in sampled_words]

    return question, answers
