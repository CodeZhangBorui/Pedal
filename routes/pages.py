"""Route of web pages."""

from flask import Blueprint, request, redirect, render_template, send_file

import orion
import functions.authentication as authed

pages = Blueprint('pages', __name__)

users = orion.Users('pedal.db', ['email'])
session = orion.Sessions('pedal.db')
permissions = orion.Permissions('pedal.db')
auditlog = orion.AuditLog('pedal.db')
configuration = orion.Configuration('pedal.db')


@pages.route('/')
def index():
    """Page for root route"""
    if authed.verify_request(request)['auth']:
        return render_template('index.html')
    return redirect('/login', code=302)

@pages.route('/favicon.ico')
def favicon():
    """Page for favicon"""
    # return send_file('static/favicon.ico')
    return {'success': False}

@pages.route('/login')
def login():
    """Page for login"""
    return render_template('login.html')

@pages.route('/account')
def account():
    """Page for account"""
    if not authed.verify_request(request)['auth']:
        return redirect('/login', code=302)
    return render_template('account.html')

@pages.route('/channels')
def channels():
    """Page for channels"""
    if not authed.verify_request(request)['auth']:
        return redirect('/login', code=302)
    if not permissions.has_permission(authed.verify_request(request)['username'], 'group.admin'):
        return redirect('/account', code=302)
    return render_template('channels.html')
