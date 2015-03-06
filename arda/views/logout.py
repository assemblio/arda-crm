from flask import session, redirect, url_for, current_app
from flask.views import View


class Logout(View):

    methods = ['POST']

    def dispatch_request(self):
        ''' Logout request.
        '''
        username = session['username']

        session.pop('username', None)
        session.pop('logged_in', None)

        current_app.logger.info("User '%s' logged out." % username)

        return redirect(url_for('index'))
