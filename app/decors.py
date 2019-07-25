from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        if True:
            return func(*args, **kwargs)
        else:
            return {'status':False, 'data':'Login Required'}
    
    return wrapper
