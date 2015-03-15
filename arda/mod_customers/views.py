from flask import Blueprint, render_template, \
                  session, redirect, url_for, current_app, request
from arda import mongo, utils
import json
from forms.customer_form import CustomerForm
from slugify import slugify
from bson import ObjectId

mod_customers = Blueprint('customers', __name__, url_prefix='/customers')


@mod_customers.route('', methods=['GET'])
def customers():
    customers = mongo.db.customers.find({})
    response = build_customers_cursor(customers)

    return render_template('mod_customers/customers.html', result=response)


@mod_customers.route('/edit', methods=['GET', 'POST'])
def edit_customer():
    form = CustomerForm()

    if request.method == "GET":
        return render_template('mod_customers/edit_customer.html', form=form)

    if request.method == "POST":
        #call the function which builds than stores the json document
        buld_save_costumers_document()

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


def buld_save_costumers_document():

    customer_form = CustomerForm(request.form)
    costumer = customer_form.data

    json_obj = {}
    json_obj = {
        'company': {
            'name': costumer['company_name'],
            'slug': slugify(costumer['company_name'])
        },
        'first_name': costumer['first_name'],
        'last_name': costumer['last_name'],
        'costumer_type': costumer['costumer_type'],
        'job_title': costumer['job_title'],
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
