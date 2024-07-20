"""Handler of APIs about clients (authentication...)."""

from flask import Blueprint, request

import orion
import functions.authentication as authed

clients = Blueprint('clients', __name__)

users = orion.Users('pedal.db', ['email'])
session = orion.Sessions('pedal.db')
permissions = orion.Permissions('pedal.db')
auditlog = orion.AuditLog('pedal.db')
configuration = orion.Configuration('pedal.db')


@clients.route('/api/clients/login', methods=['POST'])
def login():
    """API: User login."""
    try:
        username = request.json['username']
        password = request.json['password']
    except KeyError:
        return {
            'success': False,
            'message': 'Invalid request.'
        }, 400
    vrf = users.verify(username, password)
    if vrf:
        session_id = session.create(username)
        return authed.new_response({
            'success': True,
            'username': username
        }, session_id)
    else:
        return {
            'success': False,
            'message': 'Invalid username or password.'
        }
