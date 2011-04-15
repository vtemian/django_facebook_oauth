# Python
import urllib, cgi, simplejson

# Django
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Custom
from facebook.models import FacebookUser

class FacebookBackend:
    def authenticate(self, token=None, request=None):
        args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'redirect_uri': request.build_absolute_uri(reverse('facebook.views.authenticate_view')),
            'code': token,
        }
        
        target = urllib.urlopen('https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(args)).read()
        response = cgi.parse_qs(target)
        access_token = response['access_token'][-1]
        user_json = urllib.urlopen('https://graph.facebook.com/me?' + urllib.urlencode(dict(access_token=access_token)))
        fb_profile = simplejson.load(user_json)
        
        try:
            fb_user = FacebookUser.objects.get(facebook_id=str(fb_profile['id']))
        except FacebookUser.DoesNotExist:
            if request.user.is_authenticated():
                fb_user = FacebookUser(user=request.user, facebook_id=fb_profile['id'])
            else:
                request.session['fb_profile'] = fb_profile
                return None
        
        fb_user.access_token = access_token
        fb_user.save()
        
        return fb_user.user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False   





class FacebookAutoUserBackend:
    # creates a user automatically
    def authenticate(self, token=None, request=None):
        args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'redirect_uri': request.build_absolute_uri(reverse('facebook.views.authenticate_view')),
            'code': token,
        }
        
        target = urllib.urlopen('https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(args)).read()
        response = cgi.parse_qs(target)
        access_token = response['access_token'][-1]
        profile_json = urllib.urlopen('https://graph.facebook.com/me?' + urllib.urlencode(dict(access_token=access_token)))
        fb_profile = simplejson.load(profile_json)
                
        try:
            fb_user = FacebookUser.objects.get(facebook_id=str(fb_profile['id']))
        except FacebookUser.DoesNotExist:
            fb_user = FacebookUser(facebook_id=str(fb_profile['id']))

    
        fb_user.access_token = access_token
        fb_user.profile_json = str(profile_json)
                
        if not fb_user.user_id:
            try:
                fb_user.user = User.objects.get(username='fb_%s' % fb_user.facebook_id,)
            except User.DoesNotExist:
                fb_user.user = User.objects.get_or_create(
                    username='fb_%s' % fb_user.facebook_id,
                    first_name=fb_profile['first_name'],
                    last_name=fb_profile['last_name'],
                )

        fb_user.save()
        
        return fb_user.user
     
        
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False