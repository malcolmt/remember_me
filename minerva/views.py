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
    msg = ""
    form = QuestionForm(request.POST)
    if not form.is_valid():
        # FIXME: Hmm ... form tampering?! Anything legit? What to do?
        raise Exception(form.errors)
    data = form.cleaned_data
    word = Word.objects.get(id=data["meta"][0])
    query = {'word': word}
    if request.user.is_authenticated():
        query['student'] = request.user
    else:
        query['anon_student'] = request.session.session_key
    
    progress, unused = Progress.objects.get_or_create(**query)
    progress.attempts += 1
    if int(form.cleaned_data['answer']) == (word.pk):
        progress.correct += 1
        msg = "Correct. %s = %s" % (word.word, word.meaning)
    else:
        msg = "Wrong! %s = %s" % (word.word, word.meaning)
        
    progress.save()
    return msg
        
def question(request):
    context = {}
    if request.method == 'POST':
        errors = validate_answer(request)
        if errors:
            context['errors'] = errors
        
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

