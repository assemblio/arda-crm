from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, TextAreaField
from arda import mongo


class ServiceTypes(Form):
    """Service Types Form"""
    description = TextAreaField("Description")
    service_fee = IntegerField("Service Fee")
    service_date = StringField("Schedule")
    provided_service = SelectField("Provided Service")

    def __init__(self, *args, **kwargs):

        self.provided_service.kwargs['choices'] = [(item['_id']['serviceType'], item['_id']['serviceType']) for item in retrieve_all_service_types()]
        Form.__init__(self, *args, **kwargs)


def retrieve_all_service_types():
    json_result = mongo.db.servicetypes.aggregate([
        {"$unwind": "$serviceTypes"},
        {
            "$group": {
                "_id": {
                    "_id": "$_id",
                    "serviceType": "$serviceTypes.type.name",
                    "description": "$serviceTypes.description",
                }
            }
        }
    ])
    return json_result['result']
