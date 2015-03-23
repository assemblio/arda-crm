from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, TextAreaField
from arda import mongo


class ServiceTypes(Form):
    """Service Types Form"""
    description = TextAreaField("Description")
    service_fee = IntegerField("Service Fee")
    service_date = StringField("Schedule")
    provided_service = SelectField("Provided Service")
    contact_via = SelectField("Contact via")

    def __init__(self, *args, **kwargs):
        # pre-populate provided service Selectfield from database
        self.provided_service.kwargs['choices'] = [
            (
                item['_id']['serviceType'],
                item['_id']['serviceType']
            )
            for item in retrieve_all_service_types()
        ]
        # pre-populate Contact Via Selectfield from database
        self.contact_via.kwargs['choices'] = [
            (
                item['_id']['contactType'],
                item['_id']['contactType']
            )
            for item in retrieve_all_contact_types()
        ]
        Form.__init__(self, *args, **kwargs)


def retrieve_all_service_types():
    json_result = mongo.db.servicetypes.aggregate([
        {"$unwind": "$serviceTypes"},
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

def retrieve_all_contact_types():
    json_result = mongo.db.servicetypes.aggregate([
        {"$unwind": "$contactVia"},
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