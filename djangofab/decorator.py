import os
import sys
import ConfigParser
from fabric.api import *
from fabric.context_managers import *

def user_settings(file='fab.cfg', group='default'):
    "Decorator to load user settings from a config file into the env"
    def wrap(f=None):
        def wrapped_f(*args):
            f(*args)
            config = ConfigParser.ConfigParser()
            config.readfp(open(file))
            user_settings = {}
            os.environ['DJANGO_SETTINGS_MODULE'] = config.get(group,'django.settings')
            for name,value in config.items(group):
                user_settings[name] = value
            for key in env:
                if env[key] and isinstance(env[key],str):
                    env[key] = env[key] % user_settings
        return wrapped_f
    return wrap

