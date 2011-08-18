# Django + Facebook Graph API authentication
This is a django app to use the new Graph API authentication with Django. It uses the standard authentication build into Django.

Make sure you read http://developers.facebook.com/docs/authentication/ to have an idea of how this is intended to work.

## Basic setup for example project
1. Go into `./example`
2. Set up the FACEBOOK_APP_ID and FACEBOOK_APP_SECRET to your Facebook app (Set one up at https://developers.facebook.com/apps)
3. Run `python manage.py syncdb`
4. Run `python manage.py runserver`
5. Go to http://localhost:8000 and login!

## settings.py
Here are the differences between a base Django settings.py and the ones needed for the example project to run:
    AUTHENTICATION_BACKENDS = ('facebook.backend.FacebookBackend', 'django.contrib.auth.backends.ModelBackend')
    AUTH_PROFILE_MODULE = 'facebook.FacebookProfile'
    FACEBOOK_APP_ID = os.environ['FACEBOOK_APP_ID']
    FACEBOOK_APP_SECRET = os.environ['FACEBOOK_APP_SECRET']
    FACEBOOK_SCOPE = 'email,publish_stream'
    INSTALLED_APPS = ['facebook']
