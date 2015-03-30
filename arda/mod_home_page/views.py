from flask import render_template
from flask import Blueprint, render_template, \
    session, redirect, url_for, current_app, request

from arda import mongo, utils
from flask.ext.security import current_user, login_required
mod_home_page = Blueprint('home_page', __name__)


@mod_home_page.route('/', methods=['GET'])
def home_page():
    settings_doc = mongo.db.settings.find_one({'_id': 0})

    if settings_doc is None:
        session['settings'] = utils.get_default_settings()
    else:
        session['settings'] = settings_doc
    if not current_user.is_authenticated():
        return render_template('index.html')
    else:
        return redirect(url_for('home_page.panel'))


@mod_home_page.route('/panel', methods=['GET'])
@login_required
def panel():
    return render_template('panel.html')
