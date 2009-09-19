from __future__ import with_statement
from fabric.api import *
from fabric.context_managers import *
import os
import sys
#import django
from djangofab.vcs.git import do_checkout, do_push as push, do_pull as pull
from djangofab.decorator import user_settings
from djangofab.util import local_out as local, apply_settings
from django.conf import settings
#sys.path[len(sys.path):] = ['.']
#os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'

@user_settings()
def prod():
    env.hosts = ['mail']
    env.path = '%(prod_path)s'
    env.giturl = '%(giturl)s'

@user_settings()
def dev():
    env.hosts = ['mail']
    env.path = '%(dev_path)s' #% {'dev_path': '/dev/path/'}
    env.giturl = '%(giturl)s'

@user_settings('fab.cfg','local')
def localhost():
    env.path = '%(dev_path)s'
    env.giturl = '%(giturl)s'

def update():
    "pull changes from the git repository"
    #local('git pull')
    pull()

def host_type():
    "pull changes from the git repository"
#    print sys.path
#    local('echo "testing %s"' % env.giturl)
    local('echo "database %s"' % settings.DATABASE_NAME)

def test():
    local('echo "testing path = %s, settings = "' % (env.path,))
    #local('echo "testing path = %s, settings = %s"' % (env.path, os.environ['DJANGO_SETTINGS_MODULE'],))

def update_all():
    "update changes from git, update the database and build_media"
    update()
    local('bin/django clean_pyc')
    if os.path.exists('buildout.cfg'):
        local('bin/buildout')
    local('bin/django syncdb')
    if 'south' in settings.INSTALLED_APPS:
        local('bin/django migrate')
    local('bin/django build_media --all')

def deploy():
    "push local changes and update checkout on the remote host"
    push()
#    local('git push') # might fail if its not a fast forward merge
    #reset()
    checkout()
    touch_wsgi()

def checkout():
    with cd(env.path):
        do_checkout()    

def touch_wsgi():
    "Touch the wsgi file to trigger wsgi to reload the processes."
    with cd(env.path):
        run("touch bin/django.wsgi")

def get_remote_db():
    "Download the latest database from the server and load it onto your local database"
    with cd(env.path):
        if settings.DATABASE_ENGINE=='mysql': 
            run('mysqldump -u%s -p%s %s > database' %\
            (settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_NAME))
        elif settings.DATABASE_ENGINE=='postgresql' or settings.DATABASE_ENGINE=='postgresql_psycopg2':
            run('psql -u%s -p%s %s > database' %\
            (settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_NAME))
    
    get(env.path+'/database', 'database')
    if settings.DATABASE_ENGINE=='mysql': 
        local('echo "create database if not exists %s;" | mysql -u%s -p%s' %\
        (settings.DATABASE_NAME, settings.DATABASE_USER, settings.DATABASE_PASSWORD))
        local('mysql -u%s -p%s %s < database' % (settings.DATABSE_USER, settings.DATABSE_PASSWORD, settings.DATABASE_NAME))
    elif settings.DATABASE_ENGINE=='postgresql' or settings.DATABASE_ENGINE=='postgresql_psycopg2':
        run('echo "create database %s;" | psql -u%s -p%s' %\
        (settings.DATABASE_NAME, settings.DATABASE_USER, settings.DATABASE_PASSWORD))

def putlocal_db():
    "Dump your local database and load it onto the servers databse"
    if settings.DATABASE_ENGINE=='mysql': 
        local('mysqldump -u%s -p%s %s > database' %\
        (settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_NAME))
        put('database', 'database')
        local('mysql -u%s -p%s %s < database' %\
        (settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_NAME))
    elif settings.DATABASE_ENGINE=='postgresql' or settings.DATABASE_ENGINE=='postgresql_psycopg2':
        local('mysqldump -u%s -p%s %s > database' %\
        (settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_NAME))
        put('database', 'database')
        local('mysql -u%s -p%s %s < database' %\
        (settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_NAME))

