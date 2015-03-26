from flask import Blueprint, request, Response
from flask.ext.security import login_required
from arda import mongo
from bson import json_util
from datetime import datetime
from slugify import slugify

mod_api = Blueprint('api', __name__, url_prefix='/api')


@mod_api.route('/service-fee', methods=['GET'])
@login_required
def date_fee_chart():

    if(len(request.args) > 0):
        from_date = request.args.get('from')
        to_date = request.args.get('to')

    match = {}

    if from_date and to_date:
        match = {
            "$match": {
                'provided_services.service_date': {
                    '$gte': datetime.strptime(from_date, "%d-%m-%Y"),
                    '$lte': datetime.strptime(to_date, "%d-%m-%Y")
                }
            }
        }

    unwind = {
        "$unwind": "$provided_services"
    }

    group = {
        "$group": {
            "_id": {
                "serviceType": "$provided_services.provided_service.value"
            },
            'sumOfService': {
                "$sum": '$provided_services.service_fee'
            },
            'countServices': {
                "$sum": 1
            }
        }
    }

    project = {
        "$project": {
            "_id": 0,
            "serviceType": "$_id.serviceType",
            "valueOfService": "$sumOfService",
            'countServices': '$countServices'
        }
    }

    pipeline = [unwind, match, group, project]

    json_obj = mongo.db.customers.aggregate(pipeline)

    resp = Response(
        response=json_util.dumps(json_obj['result']),
        mimetype='application/json'
    )

    return resp


@mod_api.route('/search/customers', methods=['GET'])
@login_required
def search():
    if(len(request.args) > 0):
        f_name = request.args.get('firstName')
        l_name = request.args.get('lastName')
        company = request.args.get('company')
        customer_type = request.args.get('customer_type')
        print customer_type
    match_field = {}
    if f_name:
        match_field['first_name.slug'] = slugify(f_name)
    if l_name:
        match_field['last_name.slug'] = slugify(l_name)
    if company:
        match_field['company.slug'] = slugify(company)
    if customer_type:
        match_field['customer_type.target_group'] = customer_type

    match = {
        "$match": match_field
    }

    group = {
        "$group": {
            "_id": {
                "_id": "$_id",
                "target_group": "$costumer_type.target_group",
                "first_name": "$first_name.value",
                "last_name": "$last_name.value",
                "job_title": "$job_title",
                "company": {
                    "name": "$company.name",
                    "slug": "$company.slug",
                },
                "phone": {
                    "main_phone": "$phone.main_phone",
                    "mobile": "$phone.mobile",
                },
                "email": "$email",
            }
        }
    }

    project = {
        "$project": {
            "_id": 0,
            'target_group': '$_id.target_group',
            "_id": "$_id._id",
            "first_name": "$_id.first_name",
            "last_name": "$_id.last_name",
            "job_title": "$_id.job_title",
            "company": {
                "name": "$_id.company.name",
                "slug": "$_id.company.slug"
            },
            'phone': {
                "main_phone": "$_id.phone.main_phone",
                "mobile": "$_id.phone.mobile",
            },
            "email": "$_id.email",
        }
    }

    pipeline = [match, group, project]

    json_obj = mongo.db.customers.aggregate(pipeline)

    resp = Response(
        response=json_util.dumps(json_obj['result']),
        mimetype='application/json'
    )

    return resp


@mod_api.route('/search/service', methods=['GET'])
def search_service():

    if len(request.args) > 0:
        service_type = request.args.get('serviceType')
        from_dt = request.args.get('from')
        to_dt = request.args.get('to')
        contactVia = request.args.get('contactVia')

    match_fields = {}

    if contactVia:
        match_fields['provided_services.contactVia'] = contactVia

    if service_type:
        match_fields['provided_services.provided_service.slug'] = slugify(service_type)

    if from_dt and to_dt:
        match_fields['provided_services.service_date'] = {
            '$gte': datetime.strptime(from_dt, "%d/%m/%Y"),
            '$lte': datetime.strptime(to_dt, "%d/%m/%Y")
        }

    match = {
        "$match": match_fields
    }

    unwind = {
        "$unwind": "$provided_services"
    }

    group = {
        "$group": {
            "_id": {
            	'_id': '$_id',
            	"company": {
            		'name': '$company.name',
            		'slug': '$company.slug'
            	},
                "firstName": "$first_name.value",
                "lastName": "$last_name.value",
                "serviceType": "$provided_services.provided_service.value",
                'serviceId': '$provided_services.serviceId',
                'contactVia': '$provided_services.contactVia',
                "description": "$provided_services.description",
                "fee": "$provided_services.service_fee",
                "date": "$provided_services.service_date"
            }
        }
    }

    project = {
        "$project": {
            "_id": 0,
            '_id': '$_id._id',
            'company': {
            	"name": "$_id.company.name",
            	"slug": "$_id.company.slug"
            },
            "first_name": "$_id.firstName",
            "last_name": "$_id.lastName",
            "serviceType": "$_id.serviceType",
            "serviceId": "$_id.serviceId",
            "contactVia": "$_id.contactVia",
            "description": "$_id.description",
            "fee": "$_id.fee",
            "date": "$_id.date",
        }
    }

    pipeline = [unwind, match, group, project]

    json_obj = mongo.db.customers.aggregate(pipeline)

    resp = Response(
        response=json_util.dumps(json_obj['result']),
        mimetype='application/json'
    )

    return resp


@mod_api.route('/services-search', methods=['GET'])
@login_required
def search_service_analytics():

    if len(request.args) > 0:
        region = request.args.get('region')
        from_dt = request.args.get('from')
        to_dt = request.args.get('to')
        f_name = request.args.get('customerFname')
        l_name = request.args.get('customerLname')
        company = request.args.get('company')

    match_fields = {}

    if region:
        match_fields['region'] = region

    if f_name:
        match_fields['first_name.slug'] = slugify(f_name)

    if l_name:
        match_fields['last_name.slug'] = slugify(l_name)

    if company:
        match_fields['company.slug'] = slugify(company)

    if from_dt and to_dt:
        match_fields['provided_services.service_date'] = {
            '$gte': datetime.strptime(from_dt, "%d-%m-%Y"),
            '$lte': datetime.strptime(to_dt, "%d-%m-%Y")
        }

    match = {
        "$match": match_fields
    }

    unwind = {
        "$unwind": "$provided_services"
    }

    group = {
        "$group": {
            "_id": {
                "serviceType": "$provided_services.provided_service.value"
            },
            'sumOfService': {
                "$sum": '$provided_services.service_fee'
            },
            'countServices': {
                "$sum": 1
            }
        }
    }

    project = {
        "$project": {
            "_id": 0,
            "serviceType": "$_id.serviceType",
            "valueOfService": "$sumOfService",
            'countServices': '$countServices'
        }
    }

    pipeline = [unwind, match, group, project]

    json_obj = mongo.db.customers.aggregate(pipeline)

    resp = Response(
        response=json_util.dumps(json_obj['result']),
        mimetype='application/json'
    )

    return resp
