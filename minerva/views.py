from django.shortcuts import render_to_response
from minerva.questions import create_question
from django import forms

class QuestionForm(forms.Form):
    answers = forms.ChoiceField( choices=((False, 'False'), (True, 'True')), widget=forms.RadioSelect)


def question(request):
    # TODO: Things needed -
    #   - a way to select a language.
    #   - ...
    problem, answers = create_question(None, "zho", 1)
    
    form = QuestionForm()
    form.fields["answers"].choices = answers
    return render_to_response('minerva/question.html', {
        'question': problem,
        'form': form
    })
