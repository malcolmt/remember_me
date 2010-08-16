import bisect
import random

from django.conf import settings
from django.core.cache import cache
from django.db.models import Min

from minerva.models import Word
from minerva.models import SessionProgress

QUESTION_SCENARIOS = (
    # Question, answer
    ('word', 'meaning'),
    ('meaning', 'word'),
)

def get_available_words(query, language, level, last_question):
    available_words = SessionProgress.objects.filter(**query)
    if len(available_words) < 10:
        num_required = 5 - len(available_words)
        pks = word_keys(language, level)
        current_words = set(available_words.values_list("word", flat=True))
        # Collisions should be infrequent, so we should be able to get surplus
        sampled_words = set(Word.objects.filter(pk__in=random.sample(pks, num_required + 10)))
        # remove duplicate words from our candidates
        selected = sampled_words - current_words
        for i in selected:
            new_word = dict(query)
            new_word["word"] = i
            new_entry = SessionProgress.objects.create(**new_word)
        available_words = SessionProgress.objects.filter(**query)
    if last_question:
        last_word = Word.objects.get(id=last_question)
        available_words = available_words.exclude(word=last_word)
    return available_words.order_by("weight")

def decrement_weight(progress):
    if progress.weight <= 0:
        # if progress is zero we don't want to see this one again, so secretly increment
        progress.weight += 5
        progress.save()
        return
    delta = 5 + (5 * random.random())
    if progress.weight - delta < 0:
        progress.weight = 0
    else:
        progress.weight -= delta
    progress.save()

def process_answer(query_base, data):
    # FIXME - big assumption here, that the progress object exists
    correct_answer = data['meta'][0]
    query = dict(query_base)
    query['word'] = correct_answer
    progress_on_correct_answer = SessionProgress.objects.get(**query)
    if int(correct_answer) != int(data['answer']):
        # data['answer'] is the selected answer
        # Relax the weights because we got them wrong, we want to be more likely to select it next time
        query['word'] = data['answer']
        progress_on_incorrect_select = SessionProgress.objects.get(**query)
        decrement_weight(progress_on_correct_answer)
        decrement_weight(progress_on_incorrect_select)
    else:
        progress_on_correct_answer.correct += 1
        if progress_on_correct_answer.correct > 5:
            # we have seen this word enough times and answered correctly remove it from the fold
            progress_on_correct_answer.delete()
        else:
            progress_on_correct_answer.weight += 10 + (10 * random.random())
            progress_on_correct_answer.save()

def create_question_complex(query_base, language, level, last_question, num_choices=4):
    # get word with lowest weight, fill session with more words if necessary
    query = dict(query_base)
    available_words = get_available_words(query, language, level, last_question)
    query['language'] = language
    next_word = available_words[0]
    possible_answers = random.sample(available_words[1:], num_choices - 1) + [next_word]
    random.shuffle(possible_answers)
    question_attribute, answer_attribute = random.choice(QUESTION_SCENARIOS)
    question_data = (
        [next_word.word.pk, getattr(next_word.word, question_attribute)],
        [(word.word.pk, getattr(word.word, answer_attribute)) for word in possible_answers]
    )
    return question_data
    #next_word = .aggregate(Min('weight'))
    # randomly select other words from corpus

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

