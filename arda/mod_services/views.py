from flask import Blueprint, render_template, redirect, request, url_for

from arda import mongo, utils
from bson import ObjectId
from datetime import datetime
from forms.servicetypes import ServiceTypes

mod_services = Blueprint('services', __name__, url_prefix='/services')


@mod_services.route('/', methods=['GET'])
def services():

    customer = retrieve_all_services()
    return render_template('mod_services/services.html', result_services=customer)


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


@mod_services.route('/add/<company_name>/<customer_id>', methods=['GET', 'POST'])
def edit_service(company_name, customer_id):
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
            'provided_service': service_form.provided_service.data,
            'service_date': datetime.strptime(service_form.service_date.data, "%d/%m/%Y"),
            'description': service_form.description.data,
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
                        "firstName": "$first_name",
                        "lastName": "$last_name",
                        "customerId": "$_id"
                    },
                    "service": {
                        'serviceId': '$provided_services.serviceId',
                        "type": "$provided_services.provided_service",
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
                        "firstName": "$first_name",
                        "lastName": "$last_name",
                        "customerId": "$_id"
                    },
                    "service": {
                        'serviceId': '$provided_services.serviceId',
                        "type": "$provided_services.provided_service",
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
                    "type": "$_id.service.type",
                    "description": "$_id.service.description",
                    "fee": "$_id.service.fee",
                    "date": "$_id.service.date"
                }
            }
        }
    ])
    return json_obj['result']
