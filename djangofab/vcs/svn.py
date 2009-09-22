
from __future__ import with_statement
from djangofab.api import *

def update_remote():
    "Update remote checkout to the latest version"
    with cd(env.path):        
        if not remote_checkout_exists():
            run('svn co %s %s' % (env.svnurl, env.path))
        run('svn update')

def remote_export():
    "Update remote checkout to the latest version"
    with cd(env.path):
        run('svn export %s %s' % (env.svnurl, env.svnpath))

def update_local():  
    "Pull changes from version control"
    local('svn update')

def commit():
    "Save changes to version control"
    local('svn commit')

def add(file):
    "Add files to the repository"
    local('svn add %s' %file)

def checkout_local():
    local('svn co %s %s' % (env.svnurl, env.path))

def remote_checkout_exists():
    #with cd(env.path):
    out = run('ls -a | grep svn').strip()
    if out=='.svn':
        return True
    return False    
