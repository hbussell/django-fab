from __future__ import with_statement
from djangofab.api import *

def update_remote():
    "Update remote checkout to the latest version"
    with cd(env.path):
        run('git reset --hard')
        run('git pull')

def push():
    "Pull changes from version control"
    local('git push')

def update_local():  
    "Pull changes from version control"
    local('git pull')

def commit():
    "Save changes to version control"
    local('git commit -a')

def add(file):
    "Add files to the repository"
    local('git add %s' %file)
