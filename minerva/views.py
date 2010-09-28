from django.shortcuts import render_to_response
from django.template import RequestContext

from minerva.questions import create_question_complex, process_answer
from minerva.models import Progress, Word, Profile, SessionProgress
from minerva.forms import QuestionForm, ProfileForm

def validate_answer(request, query_base):
    """
    For now, just update the correct answer with the data.
    """
    # FIXME - how do I get a question form to validate across fields and
    # against the db?
    query = dict(query_base)
    form = QuestionForm(request.POST)
    if not form.is_valid():
        # Either form-tampering or submitting without data. In either case,
        # we'll just ignore it and generate a new question.
        return {}
    data = form.cleaned_data
    word = Word.objects.get(id=data["meta"][0])

    process_answer(query, data)
    query['word'] = word
    
    progress, _ = Progress.objects.get_or_create(**query)
    progress.attempts += 1
    result = {
            "prev_id": word.id,
            "prev_word": word.word,
            "prev_meaning": word.meaning
            }
    if int(form.cleaned_data['answer']) == word.pk:
        progress.correct += 1
        result["prev_result"] = True
    else:
        result["prev_result"] = False
        
    progress.save()
    return result
        
def question(request):
    context = {}
    query = {}
    if request.user.is_authenticated():
        query['student'] = request.user
        language_id = Profile.objects.get(user=request.user).language_pref_id
        if language_id is None:
            language_id = 1
    else:
        query['anon_student'] = request.session.session_key
        language_id = request.session.get('language_id', 1)

    if request.method == 'POST':
        result = validate_answer(request, query)
        context.update(result)

    # TODO: Things needed -
    #   - a way to select a language.
    #   - a way to select difficulty level.
    #   - ...
    problem, answers = create_question_complex(query, language_id, 1,
            context.get('prev_id', None))
    form = QuestionForm(question=problem, answers = answers)
    context['question'] = problem[1]
    context['form'] = form
    return render_to_response('minerva/question.html', context,
            RequestContext(request))

def status(request):
    query = {}
    if request.user.is_authenticated():
        query['student'] = request.user
    else:
        query['anon_student'] = request.session.session_key

    if request.method == 'POST':
        user_profile_form = ProfileForm(request.POST)
        if user_profile_form.is_valid():
            language_id = user_profile_form.cleaned_data['language']
            changed = False
            if request.user.is_authenticated():
                profile = Profile.objects.get(user=request.user)
                changed = profile.language_pref_id != language_id
                profile.language_pref_id = language_id
                profile.save()
            else:
                changed = request.session.get('language_id') != language_id
                request.session['language_id'] = language_id
            # clear the session progress, if our language has changed
            if changed:
                SessionProgress.objects.filter(**query).delete()
    else:
        # FIXME - move the setting of the language to the cont
        if request.user.is_authenticated():
            profile = Profile.objects.get(user=request.user)
            language_id = profile.language_pref_id
        else:
            language_id = request.session.get('language_id', '')
        user_profile_form = ProfileForm(language=language_id)
    context = {}
    progress = Progress.objects.filter(**query).order_by('-correct')
    context['progress'] = progress
    context['user_profile_form'] = user_profile_form
    return render_to_response('minerva/statistics.html', context,
            RequestContext(request))

