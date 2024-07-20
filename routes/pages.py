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

@pages.route('/login', methods=['GET'])
def login():
    """Page for login"""
    return render_template('login.html')