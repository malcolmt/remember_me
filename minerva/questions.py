from minerva.models import Word
import random

QUESTION_SCENARIOS = (
    # Question, answer
    ('word', 'meaning'),
    ('meaning', 'word'),

)

def create_question(user, language, level):
    # FIXME - maybe sanity check language
    pks = Word.objects.filter(language=language, level=level).values_list("pk", flat=True)

    sampled_pks = random.sample(pks, 4)

    sampled_words = Word.objects.filter(pk__in=sampled_pks)

    question_attribute, answer_attribute = random.choice(QUESTION_SCENARIOS)

    question = sampled_words[0].__getattribute__(question_attribute)
    answers = [i.__getattribute__(answer_attribute) for i in sampled_words]

    return question, answers
