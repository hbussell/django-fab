import os
import sys
import ConfigParser
import subprocess
from fabric.api import *
from fabric.context_managers import *

from djangofab.util import _apply_settings

def user_settings(file='fab.cfg', group='default'):
    "Decorator to load user settings from a config file into the env"
    def wrap(f=None):
        def wrapped_f(*args):
            f(*args)
            _apply_settings(file,group) 
        return wrapped_f
    return wrap


