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
                "serviceType": "$provided_services.provided_service"
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

    match_field = {}
    if f_name:
        match_field['first_name'] = f_name
    if l_name:
        match_field['last_name'] = l_name
    if company:
        match_field['company.slug'] = slugify(company)

    match = {
        "$match": match_field
    }

    group = {
        "$group": {
            "_id": {
                "_id": "$_id",
                "first_name": "$first_name",
                "last_name": "$last_name",
                "job_title": "$job_title",
                "company": {
                    "name": "$company.slug",
                    "name": "$company.name",
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
    print json_obj
    resp = Response(
        response=json_util.dumps(json_obj['result']),
        mimetype='application/json'
    )

    return resp
