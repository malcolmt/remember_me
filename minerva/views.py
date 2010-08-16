from django.shortcuts import render_to_response
from django.template import RequestContext

from minerva.questions import create_question
from minerva.models import Progress, Word
from minerva.forms import QuestionForm

def validate_answer(request):
    """
    For now just update the correct answer with the data
    FIXME - how do I get a question form to validate across fields and against the db
    """
    form = QuestionForm(request.POST)
    if not form.is_valid():
        # Either form-tampering or submitting without data. In either case,
        # we'll just ignore it and generate a new question.
        return {}
    data = form.cleaned_data
    word = Word.objects.get(id=data["meta"][0])
    query = {'word': word}
    if request.user.is_authenticated():
        query['student'] = request.user
    else:
        query['anon_student'] = request.session.session_key
    
    progress, _ = Progress.objects.get_or_create(**query)
    progress.attempts += 1
    result = {
            "prev_word": word.word,
            "prev_meaning": word.meaning
            }
    if int(form.cleaned_data['answer']) == (word.pk):
        progress.correct += 1
        result["prev_result"] = True
    else:
        result["prev_result"] = False
        
    progress.save()
    return result
        
def question(request):
    context = {}
    if request.method == 'POST':
        result = validate_answer(request)
        context.update(result)

    # TODO: Things needed -
    #   - a way to select a language.
    #   - a way to select difficulty level.
    #   - ...
    problem, answers = create_question(None, "zho", 1)
    form = QuestionForm(question=problem, answers = answers)
    context['question'] = problem[1]
    context['form'] = form
    return render_to_response('minerva/question.html', context,
            RequestContext(request))

def statistics(request):
    context = {}
    query = {}
    if request.user.is_authenticated():
        query['student'] = request.user
    else:
        query['anon_student'] = request.session.session_key
    progress = Progress.objects.filter(**query).order_by('correct').reverse()
    context['progress'] = progress
    return render_to_response('minerva/statistics.html', context,
            RequestContext(request))

