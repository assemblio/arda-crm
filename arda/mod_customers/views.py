from flask import Blueprint, render_template, \
                  session, redirect, url_for, current_app, request
from flask.ext.security import login_required
from arda import mongo, utils
import json
from forms.customer_form import CustomerForm
from slugify import slugify
from bson import ObjectId
from flask.ext.security import login_user, login_required, logout_user, current_user

mod_customers = Blueprint('customers', __name__, url_prefix='/customers')


@mod_customers.route('', methods=['GET'])
@login_required
def customers():

    customers = mongo.db.customers.find({})
    response = build_customers_cursor(customers)
    return render_template('mod_customers/customers.html', results=response)


@mod_customers.route('/create', methods=['GET', 'POST'])
def create_customer():
    form = CustomerForm()

    if request.method == "GET":
        action = url_for('customers.create_customer')
        text = "Create Contact"
        return render_template('mod_customers/edit_customer.html', form=form, action=action, text=text)

    if request.method == "POST":
        #call the function which builds than stores the json document

        build_save_costumers_document()

        return redirect(url_for('customers.customers'))



@mod_customers.route('/edit/customer/<customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):

    form = CustomerForm()
    if request.method == "GET":
        customer_doc = mongo.db.customers.find_one({'_id': ObjectId(customer_id)})

        form.company_name.data = customer_doc['company']['name']
        form.first_name.data = customer_doc['first_name']['value']
        form.last_name.data = customer_doc['last_name']['value']
        form.job_title.data = customer_doc['job_title']
        form.main_phone.data = customer_doc['phone']['main_phone']
        form.work_phone.data = customer_doc['phone']['mobile']
        form.mobile.data = customer_doc['phone']['main_phone']
        form.fax.data = customer_doc['phone']['fax']
        form.email.data = customer_doc['email']
        form.website.data = customer_doc['website']
        form.costumer_type.data = customer_doc['costumer_type']
        form.bill_add1.data = customer_doc['address']['billing']['bill_add1']
        form.bill_add2.data = customer_doc['address']['billing']['bill_add2']
        form.bill_city.data = customer_doc['address']['billing']['bill_city']
        form.bill_state.data = customer_doc['address']['billing']['bill_state']
        form.bill_postal_code.data = customer_doc['address']['billing']['bill_postal_code']
        form.bill_country.data = customer_doc['address']['billing']['bill_country']
        form.ship_add1.data = customer_doc['address']['shipping']['ship_add1']
        form.ship_add2.data = customer_doc['address']['shipping']['ship_add2']
        form.ship_city.data = customer_doc['address']['shipping']['ship_city']
        form.ship_state.data = customer_doc['address']['shipping']['ship_state']
        form.ship_postal_code.data = customer_doc['address']['shipping']['ship_postal_code']
        form.ship_country.data = customer_doc['address']['shipping']['ship_country']

        text = "Edit Contact"
        action = url_for('customers.edit_customer', customer_id=customer_id)
        return render_template(
            'mod_customers/edit_customer.html',
            form=form,
            action=action,
            text=text
        )
    elif request.method == "POST":
        edit_costumers_document(customer_id)
        return redirect(url_for('customers.customers'))

@mod_customers.route('/delete/<customer_id>', methods=['GET'])
def delete_customer(customer_id):
    mongo.db.customers.remove({'_id': ObjectId(customer_id)})

    return redirect(url_for('customers.customers'))


def build_customers_cursor(cursor):
    ''' Builds a JSON response for a given cursor
    '''
    response = json.loads('{}')
    response_to_append_to = response['results'] = []
    for idx, itm in enumerate(cursor):
        response_to_append_to.append(itm)
    return response


def build_save_costumers_document():

    customer_form = CustomerForm(request.form)
    costumer = customer_form.data

    json_obj = {}
    json_obj = {
        'company': {
            'name': costumer['company_name'],
            'slug': slugify(costumer['company_name'])
        },
        'first_name': {
        	'value': costumer['first_name'],
        	'slug': slugify(costumer['first_name']),
        },
        'last_name': {
        	'value': costumer['last_name'],
        	'slug': slugify(costumer['last_name'])
        },
        'costumer_type': costumer['costumer_type'],
        'job_title': costumer['job_title'],
        'region':  current_user['region'],
        'phone': {
            'main_phone': costumer['main_phone'],
            'work_phone': costumer['work_phone'],
            'mobile': costumer['mobile'],
            'fax': costumer['fax'],
        },
        'address': {
            'billing': {
                'bill_add1': costumer['bill_add1'],
                'bill_add2': costumer['bill_add2'],
                'bill_city': costumer['bill_city'],
                'bill_state': costumer['bill_state'],
                'bill_postal_code': costumer['bill_postal_code'],
                'bill_country': costumer['bill_country'],
            },
            'shipping': {
                'ship_add1': costumer['ship_add1'],
                'ship_add2': costumer['ship_add2'],
                'ship_city': costumer['ship_city'],
                'ship_state': costumer['ship_state'],
                'ship_postal_code': costumer['ship_postal_code'],
                'ship_country': costumer['ship_country'],
            }
        },
        'email': costumer['email'],
        'website': costumer['website'],
        'provided_services': []
    }

    mongo.db.customers.insert(json_obj)


def edit_costumers_document(customer_id):

    customer_form = CustomerForm(request.form)
    costumer = customer_form.data

    mongo.db.customers.update(
        {'_id': ObjectId(customer_id)},
        {
            "$set":{
                'company': {
                'name': costumer['company_name'],
                'slug': slugify(costumer['company_name'])
                },
                'first_name': {
                    'value': costumer['first_name'],
                    'slug': slugify(costumer['first_name']),
                },
                'last_name': {
                    'value': costumer['last_name'],
                    'slug': slugify(costumer['last_name'])
                },
                'costumer_type': costumer['costumer_type'],
                'job_title': costumer['job_title'],
                'region':  current_user['region'],
                'phone': {
                    'main_phone': costumer['main_phone'],
                    'work_phone': costumer['work_phone'],
                    'mobile': costumer['mobile'],
                    'fax': costumer['fax'],
                },
                'address': {
                    'billing': {
                        'bill_add1': costumer['bill_add1'],
                        'bill_add2': costumer['bill_add2'],
                        'bill_city': costumer['bill_city'],
                        'bill_state': costumer['bill_state'],
                        'bill_postal_code': costumer['bill_postal_code'],
                        'bill_country': costumer['bill_country'],
                    },
                    'shipping': {
                        'ship_add1': costumer['ship_add1'],
                        'ship_add2': costumer['ship_add2'],
                        'ship_city': costumer['ship_city'],
                        'ship_state': costumer['ship_state'],
                        'ship_postal_code': costumer['ship_postal_code'],
                        'ship_country': costumer['ship_country'],
                    }
                },
                'email': costumer['email'],
                'website': costumer['website'],
            }
        }
    )
