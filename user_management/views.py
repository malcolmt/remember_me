from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404

def create(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render_to_response('user_management/create.html', context, RequestContext(request))
