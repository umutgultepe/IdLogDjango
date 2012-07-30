# Create your views here.
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout

def login_page(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    mUser=request._cached_user
    if mUser.is_authenticated():
        return HttpResponseRedirect(reverse('logs.views.index'))        
    return render_to_response('authenticate/login.html', context_instance=RequestContext(request))

def success(request):
    return HttpResponseRedirect(reverse('logs.views.index'))   

def failure(request):
    return render_to_response('authenticate/login.html',{'additional_message': 'Incorrect username or password'}, context_instance=RequestContext(request))

def recieveLogin(request):
    userName = request.POST['username']
    password= request.POST['pword']
    targetUser=authenticate(username=userName, password=password)
    if targetUser is not None:
        if targetUser.is_active:
            login(request, targetUser)
            # Redirect to a success page.
            return HttpResponseRedirect(reverse('authenticate.views.success'))
        else:
            # Return a 'disabled account' error message
            return HttpResponseRedirect(reverse('authenticate.views.failure'))
    else:
        # Return an 'invalid login' error message.
        return HttpResponseRedirect(reverse('authenticate.views.failure'))
        

def logout_page(request):
    logout(request)
    return render_to_response('authenticate/login.html',{'additional_message': 'You have successfully logged out'}, context_instance=RequestContext(request))