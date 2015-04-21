from flask import Blueprint, render_template, \
    session, redirect, url_for, request

import json
from arda.mod_admin.forms.user_form import UserForm
from arda.mod_admin.forms.settings_form import SettingsForm
from arda.mod_admin.forms.portfolio_form import PortfolioForm
from arda import mongo, utils, bcrypt
from bson import ObjectId
from arda.mod_admin.models.user_model import Users
from flask.ext.security import login_required, current_user
from arda import user_datastore
from slugify import slugify

mod_admin = Blueprint('admin', __name__, url_prefix='/admin')


@mod_admin.route('/users', methods=['GET'])
@login_required
def users():
    '''
    List users
    '''
    if current_user.has_role('Admin'):
        if current_user.region != 'All':
            users = mongo.db.users.find({'region': current_user.region})
        else:
            users = mongo.db.users.find({})
        json_obj = build_contacts_cursor(users)
        return render_template('mod_admin/users.html', results=json_obj['results'])
    else:
        return redirect(url_for('customers.customers'))


@mod_admin.route('/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    '''
    Create user
    '''
    user_form = UserForm()
    # If we do a get request, we are just requesting the page.
    if request.method == "GET":
        if current_user.has_role('Admin'):
            return render_template(
                'mod_admin/edit_user.html',
                form=user_form,
                action=url_for('admin.create_user'),
                display_pass_field=False
            )
        else:
            return redirect(url_for('customers.customers'))

    elif request.method == "POST":
        if current_user.has_role('Admin'):
            user_form = UserForm(request.form)
            user_data = user_form.data
            if current_user.region == 'All':
                user = Users(
                    region=user_data['region'],
                    last_name=user_data['last_name'],
                    first_name=user_data['first_name'],
                    email=user_data['email'],
                    role=user_data['role'],
                    password=bcrypt.generate_password_hash(user_data['password'], rounds=12)
                )
            else:
                user = Users(
                    region=current_user.region,
                    last_name=user_data['last_name'],
                    first_name=user_data['first_name'],
                    email=user_data['email'],
                    role=user_data['role'],
                    password=bcrypt.generate_password_hash(user_data['password'], rounds=12)
                )
            user.save()
            default_role = user_datastore.find_role(user_data['role'])
            user_datastore.add_role_to_user(user, default_role)
            #mongo.db.users.insert(user_doc)

            return redirect(url_for('admin.users'))
        else:
            return redirect(url_for('customers.customers'))
    return render_template('mod_admin/edit_user.html', form=user_form)


@mod_admin.route('/users/edit/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    '''
    Edit user
    '''
    if request.method == "GET":
        if current_user.has_role('Admin'):
            user_doc = mongo.db.users.find_one({'_id': ObjectId(user_id)})
            # Populate the user form of the user we are editing.
            user_form = UserForm()
            user_form.first_name.data = user_doc['first_name']
            user_form.last_name.data = user_doc['last_name']
            user_form.email.data = user_doc['email']
            user_form.role.data = user_doc['role']
            user_form.region.data = user_doc['region']
            user_form.password.data = user_doc['password']

            return render_template(
                'mod_admin/edit_user.html',
                form=user_form,
                action=url_for('admin.edit_user',
                user_id=user_doc['_id'])
            )
        else:
            return redirect(url_for('home_page.panel'))
    elif request.method == "POST":
        if current_user.has_role('Admin'):
            user_form = UserForm(request.form)
            print user_form
            mongo.db.users.update(
                {'_id': ObjectId(user_id)},
                {
                    '$set': {
                        'first_name': user_form.first_name.data,
                        'last_name': user_form.last_name.data,
                        'password': bcrypt.generate_password_hash(user_form.password.data, rounds=12),
                        'region': user_form.region.data,
                        'email': user_form.email.data,
                        'role': user_form.role.data
                    }
                }
            )

            return redirect(url_for('admin.users'))
        else:
            return redirect(url_for('home_page.panel'))


@mod_admin.route('/users/delete/<user_id>', methods=['GET'])
@login_required
def delete_user(user_id):
    '''
    Delete user
    '''
    users = mongo.db.users.remove({'_id': ObjectId(user_id)})
    return redirect(url_for('admin.users'))


@mod_admin.route('/change/password', methods=['POST'])
@login_required
def change_password():
    user = mongo.db.users.find_one({'_id': ObjectId(current_user.id)})

    old_password = request.form['oldPassword']
    new_password = bcrypt.generate_password_hash(request.form['newPassword'], rounds=12)

    if not bcrypt.check_password_hash(user["password"], old_password):
        error = "Current password wrong!Password didn't change!"
        users = mongo.db.users.find({})
        json_obj = build_contacts_cursor(users)
        if current_user.has_role('Admin'):
            return render_template('mod_admin/users.html', message=error, results=json_obj['results'])
        else:
            return redirect(url_for('admin.settings'))

    else:
        mongo.db.users.update(
            {'_id': ObjectId(current_user.id)},
            {"$set": {'password': new_password}}
        )
        if current_user.has_role('Admin'):
            return redirect(url_for('admin.users'))
        else:
            return redirect(url_for('admin.settings'))


@mod_admin.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    '''
    A page to configure CRM settings (e.g. remove/add types of services)
    '''
    portfolio = None

    if request.method == 'GET':
        settings_doc = mongo.db.settings.find_one({'_id': 0})
        portfolio = []
        #retireve types in order to manage in settings page
        if current_user.region != 'All':
            query = {
                'serviceTypes.region': current_user.region
            }
            query_contact = {
                'contactVia.region': current_user.region
            }
        else:
            query = {}
            query_contact = {}

        service_type = retrieve_all_service_types(query)
        contact_via_types = retrieve_all_contact_types(query_contact)

        if settings_doc is None:
            settings_doc = utils.get_default_settings()

        elif 'portfolio' in settings_doc:
            portfolio = settings_doc['portfolio']

        settings_form = SettingsForm()
        settings_form.site_title.data = settings_doc['site_title']
        settings_form.site_tagline.data = settings_doc['site_tagline']
        settings_form.site_navbar_title.data = settings_doc['site_navbar_title']
        settings_form.web_url.data = settings_doc['web_url']
        settings_form.fb_url.data = settings_doc['fb_url']
        settings_form.tw_url.data = settings_doc['tw_url']
        settings_form.li_url.data = settings_doc['li_url']
        settings_form.support_email.data = settings_doc['support_email']

    if request.method == 'POST':
        if current_user.has_role('Admin'):
            settings_form = SettingsForm(request.form)
            settings_data = settings_form.data
            mongo.db.settings.update({'_id': 0}, {'$set': settings_data}, True)

            if current_user.region != 'All':
                query = {
                    'serviceTypes.region': current_user.region
                }
                query_contact = {
                    'contactVia.region': current_user.region
                }
            else:
                query = {}
                query_contact = {}

            service_type = retrieve_all_service_types(query)
            contact_via_types = retrieve_all_contact_types(query_contact)
            # Update session with new settings data.
            session['settings'] = settings_form.data
        else:
            return redirect(url_for('home_page.panel'))
    type_id = '5509cb3b484d3f17a2409cea'
    portfolio_form = PortfolioForm()
    return render_template(
        'mod_admin/settings.html',
        form=settings_form,
        pf_form=portfolio_form,
        portfolio=portfolio,
        service_type=service_type,
        contact_via_types=contact_via_types,
        type_id=type_id
    )


@mod_admin.route('/settings/portfolio/update', methods=['POST'])
@login_required
def settings_portfolio_update():
    if current_user.has_role('Admin'):
        portfolio_form = PortfolioForm(request.form)
        portfolio_data = portfolio_form.data
        portfolio_data['id'] = utils.get_doc_id()

        mongo.db.settings.update({'_id': 0}, {'$push': {'portfolio': portfolio_data}})
        session['settings']['portfolio'] = portfolio_data

        return redirect(url_for('admin.settings'))
    else:
        return redirect(url_for('home_page.panel'))


@mod_admin.route('/settings/portfolio/delete/<item_id>', methods=['GET'])
@login_required
def settings_portfolio_delete(item_id):
    if current_user.has_role('Admin'):
        settings = mongo.db.settings.find_one({'_id': 0})
        porfolio = []

        for item in settings['portfolio']:
            if item['id'] != item_id:
                porfolio.append(item)

        mongo.db.settings.update(
            {'_id': 0},
            {
                '$set': {
                    'portfolio':  porfolio
                }
            }
        )

        session['settings']['portfolio'] = porfolio

        return redirect(url_for('admin.settings'))
    else:
        return redirect(url_for('home_page.panel'))


@mod_admin.route('/delete/service/type/<type_id>', methods=['GET'])
@login_required
def delete_service_type(type_id):

    mongo.db.servicetypes.update(
        {},
        {
            '$pull': {
                'serviceTypes': {
                    'serviceId': ObjectId(type_id)
                }
            }
        }
    )
    return redirect(url_for('admin.settings'))


@mod_admin.route('/add/service/type/<type_id>', methods=['POST'])
@login_required
def add_service_type(type_id):
    service_type = request.form['serviceType']
    service_description = request.form['serviceDescription']
    new_type = {
        'serviceId': ObjectId(utils.get_doc_id()),
        "type": {
            "name": service_type,
            "slug": slugify(service_type)
        },
        "description": service_description
    }

    if current_user.region != 'All':
        new_type['region'] = current_user.region
    else:
        region = request.form['region']
        new_type['region'] = region

    mongo.db.servicetypes.update(
        {'_id': ObjectId(type_id)},
        {
            '$push': {
                'serviceTypes': new_type
            }
        }
    )
    return redirect(url_for('admin.settings'))


@mod_admin.route('/add/contact-via/type/<type_id>', methods=['POST'])
@login_required
def add_contact_type(type_id):
    contact_type = request.form['contactVia']
    description = request.form['contactDescription']

    new_type = {
        "type": {
            "name": contact_type,
            "slug": slugify(contact_type)
        },
        'contactId': ObjectId(utils.get_doc_id()),
        "description": description
    }

    if current_user.region != 'All':
        new_type['region'] = current_user.region
    else:
        region = request.form['region']
        new_type['region'] = region

    mongo.db.servicetypes.update(
        {'_id': ObjectId(type_id)},
        {
            '$push': {
                'contactVia': new_type
            }
        }
    )
    return redirect(url_for('admin.settings'))


@mod_admin.route('/edit/contact-via/type', methods=['POST'])
@login_required
def edit_contact_type():

    contact_type = request.form['contact_via']
    description = request.form['contact_description']
    region = request.form['cont-region']
    contact_id = request.form['contactId']

    new_type = {
        "type": {
            "name": contact_type,
            "slug": slugify(contact_type)
        },
        'region': region,
        'contactId': ObjectId(contact_id),
        "description": description
    }

    mongo.db.servicetypes.update(
        {
            "_id": ObjectId("5509cb3b484d3f17a2409cea"),
            'contactVia.contactId': ObjectId(contact_id)
        },
        {
            '$set': {
                'contactVia.$': new_type
            }
        }
    )
    return redirect(url_for('admin.settings'))


@mod_admin.route('/delete/contact-via/type/<type_id>', methods=['GET'])
@login_required
def delete_contact_type(type_id):

    mongo.db.servicetypes.update(
        {},
        {
            '$pull': {
                'contactVia': {
                    'contactId': ObjectId(type_id)
                }
            }
        }
    )
    return redirect(url_for('admin.settings'))


def build_contacts_cursor(cursor):
    ''' Builds a JSON response for a given cursor
    '''
    response = json.loads('{}')
    response_to_append_to = response['results'] = []

    for idx, itm in enumerate(cursor):
        response_to_append_to.append(itm)

    return response


def retrieve_all_service_types(query):
    json_result = mongo.db.servicetypes.aggregate([
        {"$unwind": "$serviceTypes"},
        {'$match': query},
        {
            "$group": {
                "_id": {
                    '_id': '$_id',
                    "region": "$serviceTypes.region",
                    "serviceId": "$serviceTypes.serviceId",
                    "serviceType": "$serviceTypes.type.name",
                    "description": "$serviceTypes.description"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "_id":"$_id._id",
                "region": "$_id.region",
                "serviceId": "$_id.serviceId",
                "serviceType": "$_id.serviceType",
                "description": "$_id.description",
            }
        }
    ])
    return json_result['result']


def retrieve_all_contact_types(query):
    json_result = mongo.db.servicetypes.aggregate([
        {"$unwind": "$contactVia"},
        {'$match': query},
        {
            "$group": {
                "_id": {
                    '_id': '$_id',
                    "region": "$contactVia.region",
                    "contactId": "$contactVia.contactId",
                    "contactType": "$contactVia.type.name",
                    "description": "$contactVia.description"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "_id":"$_id._id",
                "contactId": "$_id.contactId",
                "region": "$_id.region",
                "contactType": "$_id.contactType",
                "description": "$_id.description",
            }
        }
    ])
    return json_result['result']
