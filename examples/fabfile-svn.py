from __future__ import with_statement
from fabric.api import *
from fabric.context_managers import *
from django.conf import settings
from djangofab.vcs.svn import update_remote, update_local, commit, add
from djangofab.decorator import user_settings
from djangofab.util import local as local
from djangofab.django import get_remote_db, put_local_db, change_ownership, touch_wsgi
env.capture_default = False

#use the default section of fab.cfg
@user_settings()
def prod():
    "Production settings"
    env.hosts = ['mail']
    env.path = '%(prod_path)s'
    env.svnurl = '%(svnurl)s'
    env.site_user = 'owner'
    env.site_group = 'group'

@user_settings()
def dev():
    "Development settings"
    env.hosts = ['mail']
    env.path = '%(dev_path)s' #% {'dev_path': '/dev/path/'}
    env.svnurl = '%(svnurl)s'
    env.site_user = 'owner'
    env.site_group = 'group'

#use the local section
@user_settings('fab.cfg','local')
def localhost():
    "Local settings"
    env.path = '%(dev_path)s'
    env.svnurl = '%(svnurl)s'

def deploy():
    "Push local changes and update checkout on the remote host"
    update_remote() #this will update a checkout
    #remote_export() 
    change_ownership()
    touch_wsgi()
