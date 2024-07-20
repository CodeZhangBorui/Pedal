"""Common shared functions for user authentication."""

from flask import make_response

import orion

users = orion.Users('pedal.db', ['email'])
session = orion.Sessions('pedal.db')
permissions = orion.Permissions('pedal.db')
auditlog = orion.AuditLog('pedal.db')
configuration = orion.Configuration('pedal.db')

def verify_request(flask_request):
    """Verify the request is authenticated."""
    if '__session' not in flask_request.cookies:
        return {'auth': False}
    session_id = flask_request.cookies['__session']
    session_data = session.get_user(session_id)
    if session_data is None:
        return {'auth': False}
    return {'auth': True, 'username': session_data}

def new_response(response, session_id):
    """Make the response with authenticated cookies."""
    res = make_response(response)
    res.set_cookie('__session', session_id, httponly=True, max_age=43200, samesite='Strict')
    return res
