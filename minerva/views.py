from django.shortcuts import render_to_response
from django.template import RequestContext

from minerva.questions import create_question
from minerva.models import Progress, Word
from minerva.forms import QuestionForm

def validate_answer(request):
    """
    For now just update the correct answer with the data
    """
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
        query['anon_student'] = request.user
    
    progress, unused = Progress.objects.get_or_create(**query)
    progress.attempts += 1
    progress.correct += 1
    progress.save()
    #if selected_answer != correct_answer:
        

        
def question(request):
    if request.method == 'POST':
        validate_answer(request)
        
    # TODO: Things needed -
    #   - a way to select a language.
    #   - a way to select difficulty level.
    #   - ...
    problem, answers = create_question(None, "zho", 1)
    form = QuestionForm(question=problem, answers=answers)
    return render_to_response('minerva/question.html', RequestContext(request, {
        'question': problem[1],
        'form': form,
    }))
