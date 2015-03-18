from flask import Blueprint, request, Response
from flask.ext.security import login_required
from arda import mongo
from bson import json_util
from datetime import datetime
mod_api = Blueprint('api', __name__, url_prefix='/api')


@mod_api.route('/service-fee', methods=['GET'])
@login_required
def date_fee_chart():

    if(len(request.args) > 0):
        from_date = request.args.get('fromDate')
        to_date = request.args.get('toDate')

    match_dict = {}
    match_dict['provided_services'] = {}


    match = {}

    if from_date and to_date:
        match = {
            "$match":{
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
                }
            }
    }

    project = {
        "$project": {
            "_id": 0,
            "serviceType": "$_id.serviceType",
            "valueOfService": "$sumOfService"
        }
    }

    pipeline = [unwind, match, group, project]

    print pipeline

    json_obj = mongo.db.customers.aggregate(pipeline)

    resp = Response(
        response=json_util.dumps(json_obj['result']),
        mimetype='application/json'
    )

    return resp
