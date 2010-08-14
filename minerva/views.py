from django.shortcuts import render_to_response
from minerva.questions import create_question

def question(request):
    # TODO: Things needed -
    #   - a way to select a language.
    #   - ...
    problem, answers = create_question(None, "zho", 1)
    return render_to_response('minerva/question.html', {
        'question': problem,
        'answers': answers,
    })

