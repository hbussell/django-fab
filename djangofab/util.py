import os
import ConfigParser
#from djangofab.api import *
from fabric.api import *
from fabric.operations import local as _local

def local(cmd):
    if hasattr(env,'capture_default'):
        _local(cmd, env.capture_default)
    else:
        _local(cmd)

def apply_settings(file='fab.cfg', group='default'):
    if not os.path.exists(file):
        _handle_failure(message='Configuration file %s does not exist' % file)
        return
    config = ConfigParser.ConfigParser()
    config.readfp(open(file))
    user_settings = {}
    os.environ['DJANGO_SETTINGS_MODULE'] = config.get(group,'django.settings')
    for name,value in config.items(group):
        user_settings[name] = value
    for key in env:
        if env[key] and isinstance(env[key],str):
            env[key] = env[key] % user_settings

