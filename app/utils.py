import os
import random
from hashlib import sha1
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .config import SENDGRID_API_KEY


def handle_requests(actions, req, payload):

    """
    This method takes a reqest format :payload: and returns
    a response format.
    ===============
    Request Format
    ===============
    {
        "request_id" : { 
        "action_name" : {"parameter":value, ...]},
        "000" : ["action_name" ...,]
        ...
        },
        ...,
        "000" : ["request_id" ...,],
        ...
    }


    ================
    Response Format
    ================
    {
        "request_id" : { 
        "action_name" : response = {'status': True | False, 'data': ...},
        ...
        },
        ...,
    }
    """
    
    response = {}
    for request_id in payload["000"]:
        request = payload[request_id]
        response[request_id] = {}
        for action in request["000"]:
            if action in actions.keys():
                response[request_id][action] = actions[action](req, **request[action])
            else:
                response[request_id][action] = {'status':False, 'data':'Invalid Action'}
    return response


def send_email(to_email, message):

    message = Mail(
        from_email='akasanoma@example.com',
        to_emails=to_email,
        subject='Login Pin',
        html_content=f'<strong>Login code {message}</strong>')

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)


def fresh_pin():
    return ''.join([str(random.randint(0,9)) for n in range(5)])


def token(email, pin):
    return sha1(f"{pin},{email}".encode()).hexdigest()
