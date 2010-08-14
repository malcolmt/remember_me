from django.shortcuts import render_to_response
from questions import create_question
import random

def question(request):
    """
    Things needed -
     - a way to select a language selection
     - a way to 
    """
    question, answers = create_question(None, "zho", 1)
    return render_to_response('minerva/question.html', {
        'question': question,
        'answers': random.shuffle(answers),
    })
