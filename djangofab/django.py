
from __future__ import with_statement
import os
from djangofab.api import *

def get_remote_db():
    "Download the latest database from the server and load it onto your local database"
    dbsettings = get_db_settings()
    with cd(env.path):
        if dbsettings['engine']=='mysql': 
            run('mysqldump -u%(user)s -p%(pass)s %(name)s > database' % dbsettings )
        elif dbsettings['engine']=='postgresql' or dbsettings['engine']=='postgresql_psycopg2':
            run('psql -u%(user)s -p%(pass)s %(name)s > database' % dbsettings)
    
    get(env.path+'/database', 'database')
    if dbsettings['engine']=='mysql': 
        local('echo "create database if not exists %(name)s;" | mysql -u%(user)s -p%(pass)s' % dbsettings)
        local('mysql -u%(user)s -p%(pass)s %(name)s < database' % dbsettings)
    elif dbsettings['engine']=='postgresql' or dbsettings['engine']=='postgresql_psycopg2':
        run('echo "create database if not exists %(name)s;" | psql -u%(user)s -p%(pass)s' % dbsettings)

def put_local_db():
    "Dump your local database and load it onto the servers databse"
    dbsettings = get_db_settings()
    if dbsettings['engine']=='mysql': 
        local('mysqldump -u%s -p%s %s > database' %\
        (settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_NAME))
        put('database', 'database')
        local('mysql -u%s -p%s %s < database' %\
        (settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_NAME))
    elif dbsettings['engine']=='postgresql' or dbsettings['engine']=='postgresql_psycopg2':
        local('mysqldump -u%s -p%s %s > database' %\
        (settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_NAME))
        put('database', 'database')
        local('mysql -u%s -p%s %s < database' %\
        (settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_NAME))

def get_db_settings():
    try:
        from fabfile import settings
    except ImportError:
        msg = 'Please import django settings in your fabfile.py \nfrom django.conf import settings'
        _handle_failure(message=msg)
    if not 'DJANGO_SETTINGS_MODULE' in os.environ:
        msg = 'DJANGO_SETTINGS_MODULE not set \nYou must call a settings function that sets the os.environ[DJANGO_SETTINGS_MODULE] first'        
        _handle_failure(message=msg)
    if not hasattr(settings, 'DATABASE_USER'):
        # global settings is not the django settings
        msg = 'Please import django settings in your fabfile.py \nfrom django.conf import settings'        
        _handle_failure(message=msg)
    return {'user': settings.DATABASE_USER, 'pass':settings.DATABASE_PASSWORD, \
            'name':settings.DATABASE_NAME,'engine':settings.DATABASE_ENGINE}


def change_ownership():
    "Set user and group ownership on the website path"
    with cd(env.path):
        sudo('chown %s.%s -R .' % (env.site_user, env.site_group,))
        sudo('chmod ug+rw -R .')

def touch_wsgi():
    "Touch the wsgi file to trigger wsgi to reload the processes."
    with cd(env.path):
        run("touch bin/django.wsgi")

def syncdb():
    "Sync database and run"
    pass



