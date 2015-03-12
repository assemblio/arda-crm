from flask import Blueprint, render_template, \
                  session, redirect, url_for, current_app, request
from flask.views import View
import json
from arda.mod_admin.forms.user_form import UserForm
from arda.mod_admin.forms.settings_form import SettingsForm

from bson import ObjectId
from arda import mongo, utils

mod_admin = Blueprint('admin', __name__, url_prefix='/admin')

@mod_admin.route('/users', methods=['GET'])
def users():
    '''
    List users
    '''
    users = mongo.db.users.find({})
    json_obj = build_contacts_cursor(users)

    return render_template('mod_admin/users.html', results=json_obj['results'])


@mod_admin.route('/users/create', methods=['GET', 'POST'])
def create_user():
    '''
    Create user
    '''
    user_form = UserForm()

    # If we do a get request, we are just requesting the page.
    if request.method == "GET":
        return render_template(
            'mod_admin/edit_user.html',
            form=user_form,
            action=url_for('admin.create_user'),
            display_pass_field=False
        )

    elif request.method == "POST":
        user_form = UserForm(request.form)
        user_data = user_form.data
        mongo.db.users.insert(user_data)

        return redirect(url_for('admin.users'))

    return render_template('mod_admin/edit_user.html', form=user_form)


@mod_admin.route('/users/edit/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    '''
    Edit user
    '''
    if request.method == "GET":
        user_doc = mongo.db.users.find_one({'_id': ObjectId(user_id)})

        # Populate the user form of the user we are editing.
        user_form = UserForm()
        user_form.first_name.data = user_doc['first_name']
        user_form.last_name.data = user_doc['last_name']
        user_form.email.data = user_doc['email']
        user_form.role.data = user_doc['role']

        return render_template(
            'mod_admin/edit_user.html',
            form=user_form,
            action=url_for('admin.edit_user',
            user_id=user_doc['_id']),
            display_pass_field=True
        )

    elif request.method == "POST":
        user_form = UserForm(request.form)
        user_data = user_form.data

        mongo.db.users.update({'_id': ObjectId(user_id)}, {'$set': user_data})

        return redirect(url_for('admin.users'))


@mod_admin.route('/users/delete/<user_id>', methods=['GET'])
def delete_user(user_id):
    '''
    Delete user
    '''
    users = mongo.db.users.remove({'_id': ObjectId(user_id)})
    return redirect(url_for('admin.users'))


@mod_admin.route('/settings', methods=['GET', 'POST'])
def settings():
    '''
    A page to configure CRM settings (e.g. remove/add types of services)
    '''

    if request.method == 'GET':
        settings_doc = mongo.db.settings.find_one({'_id': 0})

        if settings_doc is None:
            settings_doc = utils.get_default_settings()

        settings_form = SettingsForm()
        settings_form.site_title.data = settings_doc['site_title']
        settings_form.site_tagline.data = settings_doc['site_tagline']
        settings_form.site_navbar_title.data = settings_doc['site_navbar_title']
        settings_form.landingpage_banner_image_url.data = settings_doc['landingpage_banner_image_url']
        settings_form.web_url.data = settings_doc['web_url']
        settings_form.fb_url.data = settings_doc['fb_url']
        settings_form.tw_url.data = settings_doc['tw_url']
        settings_form.li_url.data = settings_doc['li_url']

    if request.method == 'POST':
        settings_form = SettingsForm(request.form)
        settings_data = settings_form.data

        mongo.db.settings.update({'_id': 0}, {'$set': settings_data}, True)

        # Update session with new settings data.
        session['settings'] = settings_form.data

    return render_template('mod_admin/settings.html', form=settings_form)


def build_contacts_cursor(cursor):
    ''' Builds a JSON response for a given cursor
    '''
    response = json.loads('{}')
    response_to_append_to = response['results'] = []

    for idx, itm in enumerate(cursor):
        response_to_append_to.append(itm)

    return response
