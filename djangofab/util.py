import os
import sys
import ConfigParser
import subprocess
#from fabric.api import *
#from fabric.context_managers import *

from fabric.api import local as _local
from fabric.api import env


from fabric.state import env, connections, output
#def local_out(cmd):
#    return local(cmd,False)

def local(cmd):
    if hasattr(env,'capture_default'):
        _local(cmd, env.capture_default)
    else:
        _local(cmd)

def _apply_settings(file='fab.cfg', group='default'):
    config = ConfigParser.ConfigParser()
    config.readfp(open(file))
    user_settings = {}
    os.environ['DJANGO_SETTINGS_MODULE'] = config.get(group,'django.settings')
    for name,value in config.items(group):
        user_settings[name] = value
    for key in env:
        if env[key] and isinstance(env[key],str):
            env[key] = env[key] % user_settings

