from flask import Blueprint, render_template, \
                  session, redirect, url_for, current_app, request
from flask.views import View

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/login', methods=['POST'])
def login():
    '''
     Login request.
    '''
    error = None

    username = request.form['username']
    password = request.form['password']
    print username

    # If invalid username
    if username != current_app.config['USERNAME']:
        error = 'Invalid username'

    # If invalid password
    elif password != current_app.config['PASSWORD']:
        error = 'Invalid password'

    # Login success, return to index page
    else:
        session['logged_in'] = True
        session['username'] = username
        current_app.logger.info("User '%s' logged in." % username)

        return redirect('/contacts-page')

    return render_template('index.html', error=error)


@mod_auth.route('/logout', methods=['POST'])
def logout():
    ''' Logout request.
    '''
    username = session['username']

    session.pop('username', None)
    session.pop('logged_in', None)

    current_app.logger.info("User '%s' logged out." % username)

    return redirect('/')
