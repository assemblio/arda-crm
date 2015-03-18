from flask import render_template
from flask import Blueprint, render_template, \
    session, redirect, url_for, current_app, request

from arda import mongo, utils
from bson import ObjectId
mod_home_page = Blueprint('home_page', __name__)


@mod_home_page.route('/', methods=['GET'])
def home_page():
    settings_doc = mongo.db.settings.find_one({'_id': 0})
    #Create initial service types
    create_services()

    if settings_doc is None:
        session['settings'] = utils.get_default_settings()
    else:
        session['settings'] = settings_doc
    return render_template('index.html')


def create_services():
    #Create initial service types for customers
    doc_id = utils.get_doc_id()
    initial_services = [
        {
            "type": {
                "name": "Phone Call",
                "slug": "phone-call"
            },
            'serviceId': ObjectId(utils.get_doc_id()),
            "description": "Phone Call Service"
        },
        {
            "type": {
                "name": "E-mail",
                "slug": "e-mail"
            },
            'serviceId': ObjectId(utils.get_doc_id()),
            "description": "E-mail Service"
        },
        {
            "type": {
                "name": "Face-to-Face meeting",
                "slug": "face-to-face-meeting"
            },
            'serviceId': ObjectId(utils.get_doc_id()),
            "description": "Face-to-Face Service"
        }
    ]
    mongo.db.servicetypes.update(
        {'_id': ObjectId(doc_id)},
        {'$set': {"serviceTypes": initial_services}},
        True
    )
