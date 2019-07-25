from .db import User, Login
from .utils import fresh_pin, send_email, token
from .decors import login_required


def register(req, **kwargs):
    """
    :kwargs: email, device
    """

    try:
        user = User.create(email=kwargs['email'])
        login = Login.create(user=user.id, device=kwargs['device'])
        login.pin = int(f"{fresh_pin()}{login.id}")
        login.save()
        send_email(kwargs['email'], login.pin)
    except Exception as e:
        return {'status':False,'data':repr(e)}
    return {'status':True,'data':''}


def login(req, **kwargs):
    """
    :kwargs: email, fresh_pin, device
    """
    try:
        user = User.get(email=kwargs['email'])
        login = Login.get(user=user.id, pin=kwargs['fresh_pin'], device=kwargs['device'])
        if login.token:
            return {'status':False,'data':'Pin already used'}
        login.token = token(kwargs['email'], login.pin)
        login.save()
    except Exception as e:
        return {'status':False,'data':repr(e)}
    return {'status':True,'data':{'token':login.token}}



def generate_pin(req, **kwargs):
    """
    :kwargs: email, device
    """
    try:
        user = User.get(email=kwargs['email'])
        login = Login.create(user=user.id, device=kwargs['device'])
        login.pin = int(f"{fresh_pin()}{login.id}")
        login.save()
        send_email(kwargs['email'], login.pin)
    except Exception as e:
        return {'status':False,'data':repr(e)}
    return {'status':True,'data':''}


def read(req, **kwargs):
    """
    :kwargs: resource, id, data_def
    """
    return {}


@login_required
def create(req, **kwargs):
    """
    :kwargs: resource, data
    """
    return {}


@login_required
def update(req, **kwargs):
    """
    :kwargs: resource, id, data
    """
    return {}


@login_required
def delete(req, **kwargs):
    """
    :kwargs: resource, id
    """
    return {}


@login_required
def redeem_points(req, **kwargs):
    """
    :kwargs: user, phone_number
    """
    return {}


actions = {
    "create" : create,
    "read" : read,
    "update" : update,
    "delete" : delete,
    "login" : login,
    "register" : register,
    "redeem_points" : redeem_points,
    "generate_pin" : generate_pin,
}
