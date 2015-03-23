from flask import Blueprint, render_template, redirect, request, url_for

from arda import mongo, utils
from bson import ObjectId
from datetime import datetime
from forms.servicetypes import ServiceTypes
from slugify import slugify

mod_services = Blueprint('services', __name__, url_prefix='/services')


@mod_services.route('/', methods=['GET'])
def services():
    form = ServiceTypes()
    customer = retrieve_all_services()
    return render_template('mod_services/services.html', result_services=customer, form=form)


@mod_services.route('/<string:company_name>', methods=['GET'])
def company_services(company_name):
    query = {
        'company.slug': company_name
    }

    services = get_services_for_given_company(query)

    return render_template(
        'mod_services/services.html',
        company_name=company_name,
        result_services=services
    )


@mod_services.route('/<string:company_name>/<string:customer_id>', methods=['GET'])
def customer_services(company_name, customer_id):

    query = {
        'company.slug': company_name,
        '_id': ObjectId(customer_id)
    }

    customer = get_services_for_given_company(query)

    return render_template(
        'mod_services/services.html',
        company_name=company_name,
        customer_id=customer_id,
        result=customer
    )


@mod_services.route('/edit/<company_name>/<customer_id>', methods=['GET', 'POST'])
def add_service(company_name, customer_id):
    if request.method == "GET":
        form = ServiceTypes()
        return render_template(
            'mod_services/add_service.html',
            form=form,
            company_name=company_name,
            customer_id=customer_id
        )
    elif request.method == "POST":
        #services
        service_form = ServiceTypes(request.form)
        json_obj = {
            'serviceId': ObjectId(utils.get_doc_id()),
            'provided_service': {
                'value': service_form.provided_service.data,
                'slug': slugify(service_form.provided_service.data),
            },
            'service_date': datetime.strptime(service_form.service_date.data, "%d/%m/%Y"),
            'description': service_form.description.data,
            'contactVia': service_form.contact_via.data,
            'service_fee': int(service_form.service_fee.data)
        }

        mongo.db.customers.update(
            {'_id': ObjectId(customer_id)},
            {
                '$push': {
                    'provided_services': json_obj
                }
            }
        )
        return redirect(
            url_for(
                'customers.customers',
            )
        )

@mod_services.route('/edit/<company_name>/<customer_id>/<string:service_id>', methods=['GET', 'POST'])
def edit_service(company_name, customer_id, service_id):
    if request.method == "GET":
        form = ServiceTypes()
        service_doc = mongo.db.customers.find_one(
            {
                "provided_services": {
                    '$all': [
                            { "$elemMatch" : {"serviceId": ObjectId(service_id)} }
                          ] 
                }
                       
            } )
        print  service_doc['provided_services'][0]['provided_service']['value']
        form.provided_service.data = service_doc['provided_services'][0]['provided_service']['value']
        form.description.data = service_doc['provided_services'][0]['description']
        form.service_fee.data = service_doc['provided_services'][0]['service_fee']
        form.service_date.data = service_doc['provided_services'][0]['service_date']
        form.contact_via.data = service_doc['provided_services'][0]['contactVia']
    
        return render_template(
            'mod_services/add_service.html',
            form=form,
            company_name=company_name,
            customer_id=customer_id
        )
    elif request.method == "POST":
        #services
        service_form = ServiceTypes(request.form)
        json_obj = {
            'serviceId': ObjectId(utils.get_doc_id()),
            'provided_service': {
                'value': service_form.provided_service.data,
                'slug': slugify(service_form.provided_service.data),
            },
            'service_date': datetime.strptime(service_form.service_date.data, "%d/%m/%Y"),
            'description': service_form.description.data,
            'contactVia': service_form.contact_via.data,
            'service_fee': int(service_form.service_fee.data)
        }

        mongo.db.customers.update(
            {'_id': ObjectId(customer_id)},
            {
                '$push': {
                    'provided_services': json_obj
                }
            }
        )
        return redirect(
            url_for(
                'customers.customers',
            )
        )

@mod_services.route('/delete/<string:company_name>/<string:customer_id>/<string:service_id>', methods=['GET'])
def delete_service(company_name, customer_id, service_id):

    mongo.db.customers.update(
        {
            "company.slug": company_name, "_id": ObjectId(customer_id)
        },
        {
            "$pull": {
                "provided_services": {
                    'serviceId': ObjectId(service_id)}
            }
        }
    )
    return redirect(
        url_for(
            'services.customer_services',
            company_name=company_name,
            customer_id=customer_id
        )
    )


def get_services_for_given_company(query):

    json_obj = mongo.db.customers.aggregate([
        {
            "$match": query
        },
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
