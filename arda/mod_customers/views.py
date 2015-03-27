from flask import Blueprint, render_template, \
                  session, redirect, url_for, current_app, request
from flask.ext.security import login_required
from arda import mongo, utils
import json
from forms.customer_form import CustomerForm
from slugify import slugify
from bson import ObjectId
from flask.ext.security import login_user, login_required, logout_user, current_user
from arda.mod_services.forms.servicetypes import ServiceTypes
from arda.mod_customers.models.model import Customers

mod_customers = Blueprint('customers', __name__, url_prefix='/customers')


@mod_customers.route('', methods=['GET'])
@login_required
def customers():
    if not request.args.get('page'):
        page = 1
    else:
        page = int(request.args.get('page'))
    print page
    form = ServiceTypes()
    customers = mongo.db.customers.find({})
    customers_pagi = Customers.objects.all()
    pagination = customers_pagi.paginate(page=page, per_page=10)

    response = build_customers_cursor(customers)
    services = retrieve_all_services()
    return render_template('mod_customers/customers.html', pagination=pagination, result_services=services, form=form, results=response)


@mod_customers.route('/create', methods=['GET', 'POST'])
def create_customer():
    form = CustomerForm()

    if request.method == "GET":
        action = url_for('customers.create_customer')
        text = "Create Customer"
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
        print customer_doc['customer_type']['target_group']
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
        # Let's check what target group we have in order to know what fields to fill
        if customer_doc['customer_type']['target_group'] == "Entrepreneur":
            form.customer_type.data = customer_doc['customer_type']['target_group']
            form.business_name.data = customer_doc['customer_type']['business_name']
            form.vat.data = customer_doc['customer_type']['vat']
            form.fiscal_number.data = customer_doc['customer_type']['fiscal_number']
            form.legal_entity_types.data = customer_doc['customer_type']['legal_entity_types']
            form.industry.data = customer_doc['customer_type']['industry']
            form.main_activity.data = customer_doc['customer_type']['main_activity']
            form.founding_year.data = customer_doc['customer_type']['founding_year']
            form.number_of_employees.data = customer_doc['customer_type']['number_of_employees']
            form.size_category.data = customer_doc['customer_type']['size_category']
            form.investment.data = customer_doc['customer_type']['investment']
            form.business_description.data = customer_doc['customer_type']['business_description']

        elif customer_doc['customer_type']['target_group'] == "Non-Governmental Organisation":
            form.customer_type.data = customer_doc['customer_type']['target_group']
            form.ngo_registration_number_ngo.data = customer_doc['customer_type']['ngo_registration_number_ngo']
            form.vat_number_ngo.data = customer_doc['customer_type']['vat_number_ngo']
            form.fiscal_number_ngo.data = customer_doc['customer_type']['fiscal_number_ngo']
            form.sector_ngo.data = customer_doc['customer_type']['sector_ngo']
            form.founding_year_ngo.data = customer_doc['customer_type']['founding_year_ngo']
            form.number_of_staff_ngo.data = customer_doc['customer_type']['number_of_staff_ngo']
            form.description_of_ngo.data = customer_doc['customer_type']['description_of_ngo']
            form.main_activities.data = customer_doc['customer_type']['main_activities']
            form.donors.data = customer_doc['customer_type']['donors']

        else:
            form.customer_type.data = customer_doc['customer_type']['target_group']

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

        text = "Edit Customer"
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
    print costumer
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

    if current_user['region'] != "All":
    	json_obj['region'] = current_user['region']
    else:
    	json_obj['region'] = costumer['region']


    if costumer['customer_type'] == "Entrepreneur":
        json_obj['customer_type'] = {
            'target_group': costumer['customer_type'],
            'business_name': costumer['business_name'],
            'vat': costumer['vat'],
            'fiscal_number': costumer['fiscal_number'],
            'legal_entity_types': costumer['legal_entity_types'],
            'industry': costumer['industry'],
            'main_activity': costumer['main_activity'],
            'founding_year': costumer['founding_year'],
            'number_of_employees': costumer['number_of_employees'],
            'size_category': costumer['size_category'],
            'investment': costumer['investment'],
            'business_description': costumer['business_description']
        }
    elif costumer['customer_type'] == "Non-Governmental Organisation":
        json_obj['customer_type'] = {
            'target_group': costumer['customer_type'],
            'ngo_registration_number_ngo': costumer['ngo_registration_number_ngo'],
            'vat_number_ngo': costumer['vat_number_ngo'],
            'fiscal_number_ngo': costumer['fiscal_number_ngo'],
            'sector_ngo': costumer['sector_ngo'],
            'founding_year_ngo': costumer['founding_year_ngo'],
            'number_of_staff_ngo': costumer['number_of_staff_ngo'],
            'description_of_ngo': costumer['description_of_ngo'],
            'main_activities': costumer['main_activities'],
            'donors': costumer['donors']
        }
    else:
        #Investor and Municipality fields not avaliable yet
        json_obj['customer_type']={
            'target_group': costumer['customer_type']
        }

    mongo.db.customers.insert(json_obj)


def edit_costumers_document(customer_id):

    customer_form = CustomerForm(request.form)
    costumer = customer_form.data
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

    if costumer['customer_type'] == "Entrepreneur":
        json_obj['customer_type'] = {
            'target_group': costumer['customer_type'],
            'business_name': costumer['business_name'],
            'vat': costumer['vat'],
            'fiscal_number': costumer['fiscal_number'],
            'legal_entity_types': costumer['legal_entity_types'],
            'industry': costumer['industry'],
            'main_activity': costumer['main_activity'],
            'founding_year': costumer['founding_year'],
            'number_of_employees': costumer['number_of_employees'],
            'size_category': costumer['size_category'],
            'investment': costumer['investment'],
            'business_description': costumer['business_description']
        }
    elif costumer['customer_type'] == "Non-Governmental Organisation":
        json_obj['customer_type'] = {
            'target_group': costumer['customer_type'],
            'ngo_registration_number_ngo': costumer['ngo_registration_number_ngo'],
            'vat_number_ngo': costumer['vat_number_ngo'],
            'fiscal_number_ngo': costumer['fiscal_number_ngo'],
            'sector_ngo': costumer['sector_ngo'],
            'founding_year_ngo': costumer['founding_year_ngo'],
            'number_of_staff_ngo': costumer['number_of_staff_ngo'],
            'description_of_ngo': costumer['description_of_ngo'],
            'main_activities': costumer['main_activities'],
            'donors': costumer['donors']
        }
    else:
        #Investor and Municipality fields not avaliable yet
        json_obj['customer_type'] = {
            'target_group': costumer['customer_type']
        }

    mongo.db.customers.update(
        {'_id': ObjectId(customer_id)},
        {
            "$set": json_obj
                
        }
    )


def retrieve_all_services():

    json_obj = mongo.db.customers.aggregate([
        {
            "$unwind": "$provided_services"
        },
        {
            "$group": {
                "_id": {
                    '_id': '$_id',
                    "company": {
                        "name": "$company.name",
                        "slug": "$company.slug",
                    },
                    "customer": {
                        "firstName": "$first_name.value",
                        "lastName": "$last_name.value",
                        "customerId": "$_id"
                    },
                    "service": {
                        'serviceId': '$provided_services.serviceId',
                        'contactVia': '$provided_services.contactVia',
                        "type": "$provided_services.provided_service.value",
                        "description": "$provided_services.description",
                        "fee": "$provided_services.service_fee",
                        "date": "$provided_services.service_date"
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "company": {
                    "name": "$_id.company.name",
                    "slug": "$_id.company.slug",
                },
                "customer": {
                    "_id": "$_id._id",
                    "firstName": "$_id.customer.firstName",
                    "lastName": "$_id.customer.lastName",
                    "customerId": "$_id.customer.customerId",
                },
                "service": {
                    'serviceId': '$_id.service.serviceId',
                    'contactVia': '$_id.service.contactVia',
                    "type": "$_id.service.type",
                    "description": "$_id.service.description",
                    "fee": "$_id.service.fee",
                    "date": "$_id.service.date"
                }
            }
        }
    ])
    return json_obj['result']
