from djangofab.api import *
from django.conf import settings
from djangofab.vcs.git import update_remote, update_local, push, commit, add
env.capture_default = False

# apply the settings from fab.cfg default section
# sets DJANGO_SETTINGS which allows access to django.conf.settings values
apply_settings()

#use the default section of fab.cfg
@user_settings()
def prod():
    "Production settings"
    env.hosts = ['server1']
    env.path = '%(prod_path)s'
    env.giturl = '%(giturl)s'
    env.site_user = 'owner'
    env.site_group = 'group'

@user_settings()
def dev():
    "Development settings"
    env.hosts = ['server1']
    env.path = '%(dev_path)s'
    env.giturl = '%(giturl)s'
    env.site_user = 'owner'
    env.site_group = 'group'

#use the local section
@user_settings('fab.cfg','local')
def localhost():
    "Local settings"
    env.path = '%(dev_path)s'
    env.giturl = '%(giturl)s'

def deploy():
    "Push local changes and update checkout on the remote host"
    push()
    update_remote() # reset and pull on the remote server
    #remote_export() 
    change_ownership()
    touch_wsgi()

def test():    
    print "website using database %s " % (settings.DATABASE_NAME,)
    
