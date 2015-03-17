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
    if from_date:
        match_dict['provided_services.service_date'] = datetime.strptime(from_date)

    if to_date:
        match_dict['provided_services.service_date'] = datetime.strptime(to_date)

    #lets retrieve the document based in the parameter we gave
    json_obj = mongo.db.malignantdisease.aggregate([
        {
            "$unwind": "$provided_services"
        },
        {
            "$match": match_dict
        },
        {
            "$group": {
                "_id": {
                    "serviceType": "$provided_services.provided_service"
                },
                'sumOfService': {
                    "$sum": '$provided_services.service_fee'
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "serviceType": "$_id.serviceType",
                "valueOfService": "$sumOfService"
            }
        }
    ])
    print json_obj
    resp = Response(
        response=json_util.dumps(json_obj['result']),
        mimetype='application/json'
    )
    return resp
