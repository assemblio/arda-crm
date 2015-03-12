from flask import Blueprint, render_template, \
                  session, redirect, url_for, current_app, request
from arda import mongo, bcrypt

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/login', methods=['POST'])
def login():
    '''
     Login request.
    '''
    error = None

    email = request.form['email']
    password = request.form['password']

    user_doc = mongo.db.users.find_one({'email': email})
    # If invalid username
    if not user_doc:
        error = 'Invalid username'

    # If invalid password
    elif not bcrypt.check_password_hash(user_doc["password"], password):
        error = 'Invalid password'

    # Login success, return to index page
    else:
        session['logged_in'] = True
        session['email'] = email
        current_app.logger.info("User '%s' logged in." % email)

        return redirect(url_for('customers.customers'))

    return render_template('index.html', error=error)


@mod_auth.route('/logout', methods=['GET'])
def logout():
    ''' Logout request.
    '''
    email = session['email']

    session.pop('email', None)
    session.pop('logged_in', None)

    current_app.logger.info("User '%s' logged out." % email)

    return redirect(url_for('home_page.home_page'))
