
def user_settings(file='fab.cfg', group='default'):
    "Decorator to load user settings from a config file into the env"
    from djangofab.util import apply_settings
    def wrap(f=None):
        def wrapped_f(*args):
            f(*args)
            apply_settings(file,group) 
        return wrapped_f
    return wrap


