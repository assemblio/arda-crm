from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, TextField
from arda import mongo
from flask.ext.security import current_user
from checkboxwidgets import MultiCheckboxField


class ServiceTypes(Form):
    """Service Types Form"""

    description = TextAreaField("Description")
    service_fee = StringField("Service Fee")
    service_date = StringField("Schedule")
    provided_service = SelectField("Provided Service")
    provided_services_check = MultiCheckboxField("Provided Service")
    contact_via = SelectField("Contacted via")

    def __init__(self, *args, **kwargs):
        # pre-populate provided service Selectfield from database

        if current_user.region != 'All':
            query = {
                'serviceTypes.region': current_user.region
            }
            query_cont = {
                'contactVia.region': current_user.region
            }
        else:
            query = {}
            query_cont = {}

        self.provided_services_check.kwargs['choices'] = [
            (
                item['_id']['serviceType'],
                item['_id']['serviceType']
            )
            for item in retrieve_all_service_types(query)
        ]

        self.provided_service.kwargs['choices'] = [
            (
                item['_id']['serviceType'],
                item['_id']['serviceType']
            )
            for item in retrieve_all_service_types(query)
        ]
        # pre-populate Contact Via Selectfield from database
        self.contact_via.kwargs['choices'] = [
            (
                item['_id']['contactType'],
                item['_id']['contactType']
            )
            for item in retrieve_all_contact_types(query_cont)
        ]
        Form.__init__(self, *args, **kwargs)


def retrieve_all_service_types(query):

    json_result = mongo.db.servicetypes.aggregate([
        {"$unwind": "$serviceTypes"},
        {'$match': query},
        {
            "$group": {
                "_id": {
                    "_id": "$_id",
                    "serviceType": "$serviceTypes.type.name",
                    "serviceDescription": "$serviceTypes.description",
                }
            }
        }
    ])
    return json_result['result']


def retrieve_all_contact_types(query):
    json_result = mongo.db.servicetypes.aggregate([
        {"$unwind": "$contactVia"},
        {'$match': query},
        {
            "$group": {
                "_id": {
                    "_id": "$_id",
                    "contactType": "$contactVia.type.name",
                    "contactDescription": "$contactVia.description",
                }
            }
        }
    ])
    return json_result['result']
