from flask import Blueprint, render_template, \
                  session, redirect, url_for, current_app, request
from flask.views import View
import json
from arda.mod_admin.forms.user_form import UserForm
from arda.mod_admin.forms.settings_form import SettingsForm

from arda import mongo, utils

mod_admin = Blueprint('admin', __name__, url_prefix='/admin')

@mod_admin.route('/users', methods=['GET'])
def users():
    '''
    List users
    '''
    users = mongo.db.users.find({})
    json_obj = build_contacts_cursor(users)
    print json_obj['results']
    return render_template('mod_admin/users.html', result=json_obj['results'])


@mod_admin.route('/users/edit', methods=['GET', 'POST'])
def edit_user():
    '''
    Create user
    '''
    action = request.form['action']

    if request.method == 'GET':
        user_form = UserForm()

        if action == "edit":
            doc_id = request.form['docId']

            user_doc = mongo.db.users.find_one({'_id': doc_id})
            user_form.first_name.data = user_doc['first_name']
            user_form.last_name.data = user_doc['last_name']
            user_form.email.data = user_doc['email']
            user_form.role.data = user_doc['role']

        return render_template('mod_admin/edit_user.html', form=user_form)

    elif request.method == 'POST':
            user_form = UserForm(request.form)
            user_data = user_form.data
            mongo.db.users.update({'_id': docId}, {'$set': user_data}, True)

            redirect(url_for('admin.users'))


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

    if request.method == 'GET':
        settings_doc = mongo.db.settings.find_one({'_id': 0})

        settings_form = SettingsForm()
        settings_form.site_title.data = settings_doc['site_title']
        settings_form.site_tagline.data = settings_doc['site_tagline']
        settings_form.landingpage_banner_image_url.data = settings_doc['landingpage_banner_image_url']
     
    if request.method == 'POST':
        settings_form = SettingsForm(request.form)
        settings_data = settings_form.data

        mongo.db.settings.update({'_id': 0}, {'$set': settings_data}, True)

    return render_template('mod_admin/settings.html', form=settings_form)




def build_contacts_cursor(cursor):
    ''' Builds a JSON response for a given cursor
    '''
    response = json.loads('{}')
    response_to_append_to = response['results'] = []

    for idx, itm in enumerate(cursor):
        response_to_append_to.append(itm)

    return response
