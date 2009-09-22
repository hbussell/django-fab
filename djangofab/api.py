from fabric.api import *
from fabric.context_managers import *
from fabric.operations import _handle_failure
from djangofab.vcs.git import update_remote, update_local, push, commit, add
from djangofab.decorator import user_settings
from djangofab.util import local as local, apply_settings
from djangofab.django import get_remote_db, put_local_db, change_ownership, touch_wsgi

from fabric.main import _internals
_internals.append(apply_settings)
_internals.append(user_settings)
_internals.append(contextmanager)
_internals.append(nested)
_internals.append(local)
