from flask import Blueprint, render_template, redirect, request, url_for

from arda import mongo, utils
from flask.ext.security import login_user, login_required, logout_user, current_user
from bson import ObjectId
from datetime import datetime
from slugify import slugify
from forms.servicetypes import ServiceTypes
mod_services = Blueprint('services', __name__, url_prefix='/services')


@mod_services.route('/<string:company_name>', methods=['GET'])
@login_required
def company_services(company_name):
    query = {
        'company.slug': company_name
    }

    services = get_services_for_given_company(query)

    form = ServiceTypes()
    return render_template(
        'mod_services/services.html',
        company_name=company_name,
        result_services=services,
        form=form
    )


@mod_services.route('/<string:company_name>/<string:customer_id>', methods=['GET'])
@login_required
def customer_services(company_name, customer_id):

    query = {
        'company.slug': company_name,
        '_id': ObjectId(customer_id)
    }

    customer = get_services_for_given_company(query)
    form = ServiceTypes()
    return render_template(
        'mod_services/services.html',
        company_name=company_name,
        customer_id=customer_id,
        result=customer,
        form=form
    )


@mod_services.route('/create/<company_name>/<customer_id>', methods=['GET', 'POST'])
@login_required
def add_service(company_name, customer_id):
    if request.method == "GET":
        action = url_for('services.add_service', company_name=company_name, customer_id=customer_id)
        text = "Add Service"
        form = ServiceTypes()
        return render_template(
            'mod_services/add_service.html',
            form=form,
            company_name=company_name,
            customer_id=customer_id,
            text=text,
            action=action
        )
    elif request.method == "POST":
        #services
        service_form = ServiceTypes(request.form)
        json_obj = {
            'serviceId': ObjectId(utils.get_doc_id()),
            'provided_service': {
                'value': service_form.provided_service.data,
                'slug': slugify(service_form.provided_service.data),
            },
            'service_date': datetime.strptime(service_form.service_date.data, "%d/%m/%Y"),
            'description': service_form.description.data,
            'contactVia': service_form.contact_via.data,
            'service_fee': float(service_form.service_fee.data)
        }

        mongo.db.customers.update(
            {'_id': ObjectId(customer_id)},
            {
                '$push': {
                    'provided_services': json_obj
                }
            }
        )
        return redirect(
            url_for(
                'customers.customers',
            )
        )

@mod_services.route('/edit/<company_name>/<customer_id>/<string:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(company_name, customer_id, service_id):
    if request.method == "GET":
        form = ServiceTypes()
        service_doc = mongo.db.customers.aggregate([        
	        {
	            "$unwind": "$provided_services"
	        },
	        {
	            "$match": {'provided_services.serviceId': ObjectId(service_id)}
	        },
	        {
	            "$group": {
	                "_id": {
	                    "service": {
	                        'serviceId': '$provided_services.serviceId',
	                        'contactVia': '$provided_services.contactVia',
	                        "type": "$provided_services.provided_service.value",
	                        "description": "$provided_services.description",
	                        "fee": "$provided_services.service_fee",
	                        "date": "$provided_services.service_date"
	                    }
	                }
	            }
	        },
	        {
	            "$project": {
	                "_id": 0,
	                'serviceId': '$_id.service.serviceId',
	                'contactVia': '$_id.service.contactVia',
	                "type": "$_id.service.type",
	                "description": "$_id.service.description",
	                "fee": "$_id.service.fee",
	                "date": "$_id.service.date"
	            }
	        }
	    ])
        form.provided_service.data = service_doc['result'][0]['type']
        form.description.data = service_doc['result'][0]['description']
        form.service_fee.data = service_doc['result'][0]['fee']
        form.service_date.data = datetime.strftime(service_doc['result'][0]['date'], '%d/%m/%Y')
        form.contact_via.data = service_doc['result'][0]['contactVia']
        text = "Edit Service"
        action = url_for('services.edit_service', company_name=company_name, customer_id=customer_id, service_id=service_id)
        return render_template(
            'mod_services/add_service.html',
            form=form,
            company_name=company_name,
            customer_id=customer_id,
            text=text,
            action=action
        )

    elif request.method == "POST":
        #services
        service_form = ServiceTypes(request.form)
        mongo.db.customers.update(
            {
                '_id': ObjectId(customer_id),
                'provided_services.serviceId': ObjectId(service_id)
            },
            {
                '$set': {
                    'provided_services.$': {
                        'serviceId': ObjectId(service_id),
                        'provided_service': {
                            'value': service_form.provided_service.data,
                            'slug': slugify(service_form.provided_service.data),
                        },
                        'service_date': datetime.strptime(service_form.service_date.data, "%d/%m/%Y"),
                        'description': service_form.description.data,
                        'contactVia': service_form.contact_via.data,
                        'service_fee': float(service_form.service_fee.data)
                    }
                }
            }
        )
        return redirect(
            url_for(
                'customers.customers',
            )
        )

@mod_services.route('/delete/<string:company_name>/<string:customer_id>/<string:service_id>', methods=['GET'])
def delete_service(company_name, customer_id, service_id):

    mongo.db.customers.update(
        {
            "company.slug": company_name, "_id": ObjectId(customer_id)
        },
        {
            "$pull": {
                "provided_services": {
                    'serviceId': ObjectId(service_id)}
            }
        }
    )
    return redirect(
        url_for(
            'customers.customers',
        )
    )


def get_services_for_given_company(query):

    json_obj = mongo.db.customers.aggregate([
        {
            "$match": query
        },
        {
            "$unwind": "$provided_services"
        },
        {
            "$group": {
                "_id": {
                    '_id': '$_id',
                    "company": {
                        "name": "$company.name",
                        "slug": "$company.slug",
                    },
                    "customer": {
                        "firstName": "$first_name.value",
                        "lastName": "$last_name.value",
                        "customerId": "$_id"
                    },
                    "service": {
                        'serviceId': '$provided_services.serviceId',
                        'contactVia': '$provided_services.contactVia',
                        "type": "$provided_services.provided_service.value",
                        "description": "$provided_services.description",
                        "fee": "$provided_services.service_fee",
                        "date": "$provided_services.service_date"
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "company": {
                    "name": "$_id.company.name",
                    "slug": "$_id.company.slug",
                },
                "customer": {
                    "_id": "$_id._id",
                    "firstName": "$_id.customer.firstName",
                    "lastName": "$_id.customer.lastName",
                    "customerId": "$_id.customer.customerId",
                },
                "service": {
                    'serviceId': '$_id.service.serviceId',
                    'contactVia': '$_id.service.contactVia',
                    "type": "$_id.service.type",
                    "description": "$_id.service.description",
                    "fee": "$_id.service.fee",
                    "date": "$_id.service.date"
                }
            }
        }
    ])
    return json_obj['result']

def createReport():
    fn = 'report-customers.xlsx'
    workbook = xlsxwriter.Workbook(fn)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 20)
    worksheet.set_column('F:F', 20)

    worksheet.write('A1', 'Company', bold)
    worksheet.write('B1', 'First Name', bold)
    worksheet.write('C1', 'Last Name', bold)
    worksheet.write('D1', 'Target Group', bold)
    worksheet.write('E1', 'Main Phone', bold)
    worksheet.write('F1', 'E-mail', bold)

    region = current_user.region

    if region != "All":
        customers = mongo.db.customers.find({"region": region})
    else:
        customers = mongo.db.customers.find({})

    response = build_customers_cursor(customers)

    print response['results']
    i = 1
    for customer in response['results']:
        company = customer['company']['name']
        first_name = customer['first_name']['value']
        last_name = customer['last_name']['value']
        target_group = customer['customer_type']['target_group']
        phone = customer['phone']['main_phone']
        email = customer['email']

        worksheet.write(i, 0, company)
        worksheet.write(i, 1, first_name)
        worksheet.write(i, 2, last_name)
        worksheet.write(i, 3, target_group)
        worksheet.write(i, 4, phone)
        worksheet.write(i, 5, email)
        i = i + 1

    workbook.close()
    return fn


@mod_customers.route('/getXLS', methods=['POST', 'GET'])
@login_required
def getXls():
    fn = createReport()
    path = os.path.join('/home/vullkan/Desktop/dev/arda-crm', fn)
    return send_file(path, mimetype='application/vnd.ms-excel')
