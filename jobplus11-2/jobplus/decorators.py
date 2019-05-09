from flask import abort,redirect,url_for,flash
from flask_login import current_user
from functools import wraps
from jobplus.models import User

def role_required(role):

    def decorator(func):

        @wraps(func)
        def wrapper(*args,**kwrargs):
            if not current_user.is_authenticated or current_user.role < int(role):
                abort(404)
            return func(*args,**kwrargs)
        return wrapper
    return decorator

euser_requeired = role_required(User.EUSER_ROLE)
user_requeired = role_required(User.USER_ROLE)
admin_requeired = role_required(User.ADMIN_ROLE)

def role_required2(role):

    def decorator2(func):

        @wraps(func)
        def wrapper2(*args,**kwrargs):
            if not current_user.is_authenticated or current_user.role < int(role):
                flash('请登录之后再操作')
                return redirect(url_for('front.login'))
            return func(*args,**kwrargs)
        return wrapper2
    return decorator2

user_requeired2 = role_required2(User.USER_ROLE)

