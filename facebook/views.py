import urllib

from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate

def login(request):
    """ First step of process, redirects user to facebook, which redirects to authentication_callback. """

    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
        'redirect_uri': request.build_absolute_uri('/facebook/authentication_callback'),
    }
    return HttpResponseRedirect('https://www.facebook.com/dialog/oauth?' + urllib.urlencode(args))

def authentication_callback(request):
    """ Second step of the login process.
    It reads in a code from Facebook, then redirects back to the home page. """
    code = request.GET.get('code')
    user = authenticate(token=code, request=request)
    auth_login(request, user)
    return HttpResponseRedirect('/')
