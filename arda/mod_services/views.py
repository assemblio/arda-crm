from flask import Blueprint, render_template, redirect, request, url_for

from arda import mongo
mod_services = Blueprint('services', __name__, url_prefix='/services')


@mod_services.route('/', methods=['GET'])
def services():

    customer = mongo.db.customers.find({})

    return render_template('mod_services/services.html', result=customer)


@mod_services.route('/<string:company_name>', methods=['GET'])
def company_services(company_name):

    query = {
        'company_name': company_name
    }

    customer = mongo.db.customers.find(query)

    return render_template('mod_services/services.html', result=customer)


@mod_services.route('/<string:company_name>/<string:customer_id>', methods=['GET'])
def customer_services(company_name, customer_id):

    query = {
        'company_name': company_name,
        '_id': customer_id
    }

    customer = mongo.db.customers.find_one(query)
    print customer

    return render_template('mod_services/services.html', result=customer)


@mod_services.route('/edit', methods=['POST'])
def edit_service():

    costumer_id = request.form['costumer_id']
    provided_service = request.form['providedService']
    date = request.form['date']
    description = request.form['description']
    service_fee = request.form['fee']

    json_obj = {
        'provided_service': provided_service,
        'service_date': date,
        'description': description,
        'service_fee': service_fee
    }

    mongo.db.customers.update(
        {'_id': costumer_id},
        {
            '$addToSet': {
                'provided_services': json_obj
            }
        }
    )
    return redirect(url_for('services.customer_services', company_name='assemblio', customer_id=costumer_id))
