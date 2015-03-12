from flask import Blueprint, render_template, \
                  session, redirect, url_for, current_app, request
from flask.views import View

from arda.mod_admin.forms.user_form import UserForm
from arda.mod_admin.forms.settings_form import SettingsForm
from arda.mod_admin.forms.theme_form import ThemeForm

mod_admin = Blueprint('admin', __name__, url_prefix='/admin')

@mod_admin.route('/users', methods=['GET'])
def users():
    '''
    List users
    '''
    users = mongo.db.users.find({})

    return render_template('mod_admin/users.html', result=users)

@mod_admin.route('/users/edit', methods=['GET', 'POST'])
def edit_user():
    '''
    Create user
    '''
    user_form = UserForm()
    return render_template('mod_admin/edit_user.html', form=user_form)


@mod_admin.route('/users/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    '''
    Delete user
    '''
    users = mongo.db.users.find({})

    return render_template('mod_admin/users.html', result=users)


@mod_admin.route('/settings', methods=['GET', 'POST'])
def settings():
    '''
    A page to configure CRM settings (e.g. remove/add types of services)
    '''
    # if GET request, do nothing.
    # if POST request, get form values and update document

    #TODO Populate form.
    settings_form = SettingsForm()

    return render_template('mod_admin/settings.html', form=settings_form)



@mod_admin.route('/theme', methods=['GET', 'POST'])
def theme():
    '''
    A page to configure CRM theme (e.g. website title, images, etc)
    '''

    # if GET request, do nothing.
    # if POST request, get form values and update document

    #TODO Populate form.
    themes_form = ThemesForm()


    return render_template('mod_admin/theme.html', form=themes_form)
