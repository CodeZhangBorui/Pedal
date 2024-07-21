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

@clients.route('/api/clients/logout', methods=['POST'])
def logout():
    """API: User logout."""
    vrf = authed.verify_request(request)
    if vrf['auth']:
        session.delete(vrf['session_id'])
        return {
            'success': True
        }
    else:
        return {
            'success': False,
            'message': 'Not authenticated.'
        }, 401

@clients.route('/api/clients/changepass', methods=['POST'])
def changepass():
    """API: Change password."""
    vrf = authed.verify_request(request)
    if not vrf['auth']:
        return {
            'success': False,
            'message': 'Not authenticated.'
        }, 401
    try:
        old_password = request.json['oldpass']
        new_password = request.json['newpass']
    except KeyError:
        return {
            'success': False,
            'message': 'Invalid request.'
        }, 400
    if not users.verify(vrf['username'], old_password):
        return {
            'success': False,
            'message': 'Invalid old password.'
        }
    users.update(vrf['username'], passwd=new_password)
    session.purge_user(vrf['username'])
    return {
        'success': True
    }


@clients.route('/api/clients/account', methods=['GET'])
def account():
    """API: Get account information."""
    vrf = authed.verify_request(request)
    if not vrf['auth']:
        return {
            'success': False,
            'message': 'Not authenticated.'
        }, 401
    account_data = users.get_by_name(vrf['username'])
    perm_level = 'default'
    if permissions.has_permission(vrf['username'], 'admin'):
        perm_level = 'admin'
    return {
        'success': True,
        'username': vrf['username'],
        'email': account_data['email'],
        'permission': perm_level
    }