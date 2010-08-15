from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from minerva.forms import UserProfileForm

def create_user(request):
    if request.method == 'POST':
        user_create_form = UserCreationForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)
        if user_create_form.is_valid():
            user_create_form.save()
            if user_profile_form.is_valid():
                user_profile_form.save()
            return HttpResponseRedirect('/login/')
    else:
        user_create_form = UserCreationForm()
        user_profile_form = UserProfileForm()
    context = {
        'user_create_form': user_create_form,
        'user_profile_form': user_profile_form
    }
    return render_to_response('user_management/create.html', context,
            RequestContext(request))

