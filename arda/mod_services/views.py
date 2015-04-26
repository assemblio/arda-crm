from flask import Blueprint, render_template, redirect, request, url_for, send_file, current_app
from flask.ext.security import login_required, current_user
from arda import mongo, utils
from bson import ObjectId
import datetime
from slugify import slugify
from forms.servicetypes import ServiceTypes
from flask.ext.mongoengine import Pagination
import xlsxwriter
import os

mod_services = Blueprint('services', __name__, url_prefix='/services')


@mod_services.route('', methods=['GET'])
def services():
    if not request.args.get('page'):
        page = 1
    else:
        page = int(request.args.get('page'))
    form = ServiceTypes()
    region = current_user.region
    services = retrieve_all_services(region)

    pagination_services = Pagination(services, page=page, per_page=10)
    form = ServiceTypes()
    if current_user.region != 'All':
            query = {
                "$or": [
                    {'serviceTypes.region': current_user.region},
                    {'serviceTypes.region': "All"}
                ]
            }
    else:
            query = {}
    service_type = retrieve_all_service_types(query)
    return render_template(
        'mod_services/services.html',
        service_type=service_type,
        pagination_services=pagination_services,
        form=form
    )


@mod_services.route('/<string:company_name>', methods=['GET'])
@login_required
def company_services(company_name):
    if current_user.region != 'All':
        query = {
            'company.slug': company_name,
            'region': current_user.region
        }
    else:
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

    if current_user.region != 'All':
        query = {
            'company.slug': company_name,
            '_id': ObjectId(customer_id),
            'region': current_user.region
        }
    else:
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
            'service_date': datetime.datetime.strptime(service_form.service_date.data, "%d/%m/%Y"),
            'description': service_form.description.data,
            'contactVia': service_form.contact_via.data,
            'unit_param': service_form.unit_param.data,
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
                            "unit": "$provided_services.unit_param",
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
                    "unit": "$_id.service.unit",
                    "date": "$_id.service.date"
                }
            }
        ])
        form.provided_service.data = service_doc['result'][0]['type']
        form.description.data = service_doc['result'][0]['description']
        form.service_fee.data = service_doc['result'][0]['fee']
        form.service_date.data = datetime.datetime.strftime(service_doc['result'][0]['date'], '%d/%m/%Y')
        form.contact_via.data = service_doc['result'][0]['contactVia']
        form.unit_param.data = service_doc['result'][0]['unit']
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
                        'service_date': datetime.datetime.strptime(service_form.service_date.data, "%d/%m/%Y"),
                        'description': service_form.description.data,
                        'contactVia': service_form.contact_via.data,
                        'unit_param': service_form.unit_param.data,
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
@login_required
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


def retrieve_all_services(region):

    if region != 'All':
        match = {
            '$match': {'region': region}
        }
    else:
        match = {
            '$match': {}
        }
    unwind = {
        "$unwind": "$provided_services"
    }

    group = {
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
    }

    project = {
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

    pipeline = [unwind, match, group, project]
    json_obj = mongo.db.customers.aggregate(pipeline)
    return json_obj['result']


def retrieve_all_service_types(query):
    json_result = mongo.db.servicetypes.aggregate([
        {"$unwind": "$serviceTypes"},
        {'$match': query},
        {
            "$group": {
                "_id": {
                    '_id': '$_id',
                    'region': '$serviceTypes.region',
                    "serviceId": "$serviceTypes.serviceId",
                    "serviceType": "$serviceTypes.type.name",
                    "description": "$serviceTypes.description"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "_id": "$_id._id",
                'region': '$_id.region',
                "serviceId": "$_id.serviceId",
                "serviceType": "$_id.serviceType",
                "description": "$_id.description",
            }
        }
    ])
    return json_result['result']


def create_report_services():
    fn = '%s/All Services.xlsx' % current_app.config['EXCEL_DOC_DIR']

    workbook = xlsxwriter.Workbook(fn)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    center = workbook.add_format({'align': 'center'})

    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 15)
    worksheet.set_column('F:F', 15)
    worksheet.set_column('G:G', 15)
    worksheet.set_column('H:H', 15)

    worksheet.write('A1', 'Company', bold)
    worksheet.write('B1', 'First Name', bold)
    worksheet.write('C1', 'Last Name', bold)
    worksheet.write('D1', 'Service Type', bold)
    worksheet.write('E1', 'Contacted Via', bold)
    worksheet.write('F1', 'Service Date', bold)
    worksheet.write('G1', 'Service Fee', bold)
    worksheet.write('H1', 'Service Description', bold)

    region = current_user.region
    response = retrieve_all_services(region)

    i = 1
    for service in response:
        company = service['company']['name']
        first_name = service['customer']['firstName']
        last_name = service['customer']['lastName']
        service_type = service['service']['type']
        contact_via = service['service']['contactVia']
        service_date = service['service']['date']
        service_fee = service['service']['fee']
        service_description = service['service']['description']

        worksheet.write(i, 0, company, center)
        worksheet.write(i, 1, first_name, center)
        worksheet.write(i, 2, last_name, center)
        worksheet.write(i, 3, service_type, center)
        worksheet.write(i, 4, contact_via, center)
        worksheet.write(i, 5, str(service_date))
        worksheet.write(i, 6, service_fee, center)
        worksheet.write(i, 7, service_description, center)
        i = i + 1

    workbook.close()
    return fn


@mod_services.route('/export-services', methods=['POST', 'GET'])
@login_required
def export_services():
    fn = create_report_services()
    path = os.path.join(current_app.config['EXCEL_DOC_DIR'], fn)
    return send_file(path, mimetype='application/vnd.ms-excel')

'''
def get_timestamp():
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    return timestamp
'''

def create_filtered_report_services(response):
    fn = '%s/All Filtered Services.xlsx' % current_app.config['EXCEL_DOC_DIR']

    workbook = xlsxwriter.Workbook(fn)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    center = workbook.add_format({'align': 'center'})

    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 15)
    worksheet.set_column('F:F', 15)
    worksheet.set_column('G:G', 15)
    worksheet.set_column('H:H', 15)

    worksheet.write('A1', 'Company', bold)
    worksheet.write('B1', 'First Name', bold)
    worksheet.write('C1', 'Last Name', bold)
    worksheet.write('D1', 'Service Type', bold)
    worksheet.write('E1', 'Contacted Via', bold)
    worksheet.write('F1', 'Service Date', bold)
    worksheet.write('G1', 'Service Fee', bold)
    worksheet.write('H1', 'Service Description', bold)

    i = 1
    for service in response:
        company = service['company']['name']
        first_name = service['customer']['firstName']
        last_name = service['customer']['lastName']
        service_type = service['service']['type']
        contact_via = service['service']['contactVia']
        service_date = service['service']['date']
        service_fee = service['service']['fee']
        service_description = service['service']['description']

        worksheet.write(i, 0, company, center)
        worksheet.write(i, 1, first_name, center)
        worksheet.write(i, 2, last_name, center)
        worksheet.write(i, 3, service_type, center)
        worksheet.write(i, 4, contact_via, center)
        worksheet.write(i, 5, str(service_date))
        worksheet.write(i, 6, service_fee, center)
        worksheet.write(i, 7, service_description, center)
        i = i + 1

    workbook.close()
    return fn


@mod_services.route('/export-filtered-services', methods=['GET'])
@login_required
def export_filtered_services():
    if(len(request.args) > 0):
        year = request.args.get('year')
        month = request.args.get('month')
        service_type = request.args.get('serviceType')

    match_fields = {}

    region = current_user.region

    if region != "All":
        match_fields['region'] = region
    if year:
        start_date = "01-01-%s" % year
        end_date = "31-12-%s" % year
        match_fields["provided_services.service_date"] = {
            '$gte': datetime.datetime.strptime(start_date, "%d-%m-%Y"),
            '$lte': datetime.datetime.strptime(end_date, "%d-%m-%Y")
        }

    if month:
        if month != "All":
            start_date = "01-%s-%s" % (month, year)
            months_with_31 = [1, 3, 5, 7, 8, 10, 12]
            if month == 2:
                end_date = "28-%s-%s" % (month, year)
            elif month in months_with_31:
                end_date = "31-%s-%s" % (month, year)
            else:
                end_date = "30-%s-%s" % (month, year)

            match_fields['provided_services.service_date'] = {
                '$gte': datetime.datetime.strptime(start_date, "%d-%m-%Y"),
                '$lte': datetime.datetime.strptime(end_date, "%d-%m-%Y")
            }
    if service_type:
        match_fields["provided_services.provided_service.slug"] = slugify(service_type)

    match = {

        "$match": match_fields
    }
    unwind = {
        "$unwind": "$provided_services"
    }

    group = {
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
    }

    project = {
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

    pipeline = [unwind, match, group, project]
    json_obj = mongo.db.customers.aggregate(pipeline)
    json_filtered = json_obj['result']

    print json_filtered
    fn = create_filtered_report_services(json_filtered)
    path = os.path.join(current_app.config['EXCEL_DOC_DIR'], fn)
    return send_file(path, mimetype='application/vnd.ms-excel')
