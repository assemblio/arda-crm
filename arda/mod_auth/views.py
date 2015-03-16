from flask import Blueprint, render_template, \
    session, redirect, url_for, current_app, request
from arda import mongo, bcrypt
from bson import json_util, ObjectId
from arda.mod_admin.models.user_model import Users, Role
from flask.ext.security import login_user, login_required, logout_user
from mongoengine import DoesNotExist

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/login', methods=['POST'])
def login():
    '''
     Login request.
    '''
    error = None

    email = request.form['email']
    password = request.form['password']

    user_doc = Users.objects.get(email=email)
    # If invalid username
    if not user_doc:
        error = 'Invalid username'

    # If invalid password
    elif not bcrypt.check_password_hash(user_doc["password"], password):
        error = 'Invalid password'

    # Login success, return to index page
    else:
        login_user(user_doc)
        current_app.logger.info("User '%s' logged in." % email)

        return redirect(url_for('customers.customers'))

    return render_template('index.html', error=error)


@mod_auth.route('/logout', methods=['GET'])
@login_required
def logout():
    ''' Logout request.
    '''
    logout_user()
    #current_app.logger.info("User '%s' logged out." % email)
    return redirect(url_for('home_page.home_page'))
