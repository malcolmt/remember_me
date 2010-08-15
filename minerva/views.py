from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms

from minerva.questions import create_question
from minerva.models import Progress, Word

class QuestionForm(forms.Form):
    answers = forms.ChoiceField(choices=((False, 'False'), (True, 'True')), widget=forms.RadioSelect)
    question_meta = forms.CharField(initial="bleh", widget=forms.HiddenInput)
    def __init__(self, *args, **kwargs):
        answers = kwargs.pop('answers', None)
        meta = kwargs.pop('meta', None)
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['answers'].choices = answers
        self.fields['question_meta'].initial = meta

def pack_question_meta_data(correct_answer_pk, answers_pk):
    # flatten the question meta data
    data = []
    data.append(str(correct_answer_pk))
    data.extend([str(i) for i in answers_pk])
    return "|".join(data)
    

def unpack_question_meta_data(packed_data):
    data = [int(i) for i in packed_data.split("|")]
    return data[0], data[1:]

def validate_answer(request):
    """
    For now just update the correct answer with the data
    """
    post_data = request.POST
    selected_answer = post_data["answers"]
    correct_answer, answers = unpack_question_meta_data(post_data["question_meta"])
    word = Word.objects.get(id=correct_answer)
    query = {'word': word}
    if request.user.is_authenticated():
        query['student'] = request.user
    else:
        query['anon_student'] = request.session.session_key
    
    progress = Progress.objects.filter(**query)
    if not progress:
        progress = Progress.objects.create(**query)
    else:
        progress = Progress.objects.get(**query)
        
    progress.attempts += 1
    progress.correct += 1
    progress.save()
        
def question(request):
    # TODO: Things needed -
    #   - a way to select a language.
    if request.method == 'POST':
        validate_answer(request)
        
    problem, answers = create_question(None, "zho", 1)
    meta = pack_question_meta_data(answers[0][0], [i[0] for i in answers])
    form = QuestionForm(answers = answers, meta = meta)
    return render_to_response('minerva/question.html', RequestContext(request, {
        'question': problem,
        'form': form,
    }))
