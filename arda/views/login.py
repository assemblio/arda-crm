from flask import session, request, render_template, redirect, current_app, url_for
from flask.views import View


class Login(View):

    methods = ['POST']

    def dispatch_request(self):
        ''' Login request.
        '''
        error = None

        username = request.form['username']
        password = request.form['password']

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

            return redirect(url_for('index'))

        return render_template('index.html', error=error)
