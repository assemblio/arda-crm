from flask import Blueprint, url_for, request, redirect, render_template

from arda import mongo
mod_analytics = Blueprint('analytics', __name__, url_prefix='/analytics')


@mod_analytics.route('', methods=['GET'])
def analytics():
    services_incomes = provided_services_incomes()
    return render_template('mod_analytics/analytics.html', results=services_incomes)


def provided_services_incomes():

    json_obj = mongo.db.customers.aggregate([
        {
            "$unwind": "$provided_services"
        },
        {
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
        },
        {
            "$project": {
                "_id": 0,
                "serviceType": "$_id.serviceType",
                "valueOfService": "$sumOfService",
                'countServices': '$countServices'
            }
        }
    ])
    return json_obj['result']
