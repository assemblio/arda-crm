from flask import Blueprint, render_template, redirect, request, url_for

from arda import mongo
mod_provided_services = Blueprint('provided_services', __name__, url_prefix='/provided-services')


@mod_provided_services.route('/<string:contact_id>', methods=['GET'])
def provided_services(contact_id):
    costumer_doc = mongo.db.contacts.find_one({"_id": contact_id})

    return render_template('mod_services/provided_services.html', result=costumer_doc)


@mod_provided_services.route('/new', methods=['POST'])
def new_services():

    costumer_id = request.form['costumer_id']
    provided_service = request.form['providedService']
    date = request.form['date']
    description = request.form['description']
    json_obj = {
        'provided_service': provided_service,
        'service_date': date,
        'description': description
    }
    mongo.db.contacts.update(
        {'_id': costumer_id},
        {
            '$addToSet': {
                'provided_services': json_obj
            }
        }
    )
    build_url_rule = '/provided-services/' + costumer_id
    return redirect(build_url_rule)
