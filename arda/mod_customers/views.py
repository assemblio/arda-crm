from flask import Blueprint, send_file, render_template, \
    redirect, url_for, current_app, request
import os
from arda import mongo
import xlsxwriter
import json
from forms.customer_form import CustomerForm
from slugify import slugify
from bson import ObjectId
from flask.ext.security import login_required, current_user
from arda.mod_services.forms.servicetypes import ServiceTypes
from arda.mod_customers.models.model import Customers
from flask.ext.mongoengine import DoesNotExist


mod_customers = Blueprint('customers', __name__, url_prefix='/customers')


@mod_customers.route('', methods=['GET'])
@login_required
def customers():
    if not request.args.get('page'):
        page = 1
    else:
        page = int(request.args.get('page'))
    form = CustomerForm()
    customers = mongo.db.customers.find({})

    try:
        customers_pagi = Customers.objects.all()
        pagination = customers_pagi.paginate(page=page, per_page=100)

    except DoesNotExist:

        pagination = None

    response = build_customers_cursor(customers)

    return render_template(
        'mod_customers/customers.html',
        pagination=pagination,
        form=form,
        results=response
    )


@mod_customers.route('/create', methods=['GET', 'POST'])
@login_required
def create_customer():
    form = CustomerForm()

    if request.method == "GET":
        action = url_for('customers.create_customer')
        text = "Create a New Customer"
        return render_template(
            'mod_customers/edit_customer.html',
            form=form,
            action=action,
            text=text
        )

    if request.method == "POST":
        #call the function which builds than stores the json document

        build_save_costumers_document()

        return redirect(url_for('customers.customers'))


@mod_customers.route('/edit/customer/<customer_id>', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):

    form = CustomerForm()
    if request.method == "GET":
        customer_doc = mongo.db.customers.find_one({'_id': ObjectId(customer_id)})

        if customer_doc['region'] == 'West':
            form.municipality_region_west.data = customer_doc['municipality_region']

        if customer_doc['region'] == 'Center':
            form.municipality_region_central.data = customer_doc['municipality_region']

        if customer_doc['region'] == 'East':
            form.municipality_region_east.data = customer_doc['municipality_region']

        if customer_doc['region'] == 'South':
            form.municipality_region_south.data = customer_doc['municipality_region']

        if customer_doc['region'] == 'North':
            form.municipality_region_north.data = customer_doc['municipality_region']

        form.company_name.data = customer_doc['company']['name']
        form.first_name.data = customer_doc['first_name']['value']
        form.last_name.data = customer_doc['last_name']['value']
        form.job_title.data = customer_doc['job_title']
        form.main_phone.data = customer_doc['phone']['main_phone']
        form.work_phone.data = customer_doc['phone']['mobile']
        form.mobile.data = customer_doc['phone']['main_phone']
        form.fax.data = customer_doc['phone']['fax']
        form.email.data = customer_doc['email']
        form.region.data = customer_doc['region']
        form.customer_address.data = customer_doc['customer_address']
        form.website.data = customer_doc['website']
        # Let's check what target group we have in order to know what fields to fill
        if customer_doc['customer_type']['target_group'] == "Entrepreneur":
            form.customer_type.data = customer_doc['customer_type']['target_group']
            form.business_name.data = customer_doc['customer_type']['business_name']
            form.vat.data = customer_doc['customer_type']['vat']
            form.fiscal_number.data = customer_doc['customer_type']['fiscal_number']
            form.legal_entity_types.data = customer_doc['customer_type']['legal_entity_types']
            form.industry.data = customer_doc['customer_type']['industry']
            form.main_activity.data = customer_doc['customer_type']['main_activity']
            form.founding_year.data = customer_doc['customer_type']['founding_year']
            form.number_of_employees.data = customer_doc['customer_type']['number_of_employees']
            form.size_category.data = customer_doc['customer_type']['size_category']
            form.investment.data = customer_doc['customer_type']['investment']
            form.business_description.data = customer_doc['customer_type']['business_description']

        elif customer_doc['customer_type']['target_group'] == "Non-Governmental Organisation":
            form.customer_type.data = customer_doc['customer_type']['target_group']
            form.ngo_registration_number_ngo.data = customer_doc['customer_type']['ngo_registration_number_ngo']
            form.vat_number_ngo.data = customer_doc['customer_type']['vat_number_ngo']
            form.fiscal_number_ngo.data = customer_doc['customer_type']['fiscal_number_ngo']
            form.sector_ngo.data = customer_doc['customer_type']['sector_ngo']
            form.founding_year_ngo.data = customer_doc['customer_type']['founding_year_ngo']
            form.number_of_staff_ngo.data = customer_doc['customer_type']['number_of_staff_ngo']
            form.description_of_ngo.data = customer_doc['customer_type']['description_of_ngo']
            form.main_activities.data = customer_doc['customer_type']['main_activities']
            form.donors.data = customer_doc['customer_type']['donors']

        elif customer_doc['customer_type']['target_group'] == "Investor":
            form.customer_type.data = customer_doc['customer_type']['target_group']
            form.country.data = customer_doc['customer_type']['country']
            form.business.data = customer_doc['customer_type']['business']
            form.business_number.data = customer_doc['customer_type']['business_number']
            form.interest.data = customer_doc['customer_type']['interest']
            form.investor_industry.data = customer_doc['customer_type']['investor_industry']
            form.industry_of_interest.data = customer_doc['customer_type']['industry_of_interest']
            form.investor_size.data = customer_doc['customer_type']['investor_size']
            form.foundation_year_investor.data = customer_doc['customer_type']['foundation_year_investor']
            form.description_investor.data = customer_doc['customer_type']['description_investor']

        else:
            form.customer_type.data = customer_doc['customer_type']['target_group']
            form.municipality_name.data = customer_doc['customer_type']['municipality_name']
            form.department.data = customer_doc['customer_type']['department']
            form.offering.data = customer_doc['customer_type']['offering']
            form.industries.data = customer_doc['customer_type']['industries']
            form.modules.data = customer_doc['customer_type']['modules']
            form.infrastructure_available.data = customer_doc['customer_type']['infrastructure_available']
            form.investment_incentives.data = customer_doc['customer_type']['investment_incentives']
            form.description.data = customer_doc['customer_type']['description']

        form.bill_add1.data = customer_doc['address']['billing']['bill_add1']
        form.bill_add2.data = customer_doc['address']['billing']['bill_add2']
        form.bill_city.data = customer_doc['address']['billing']['bill_city']
        form.bill_state.data = customer_doc['address']['billing']['bill_state']
        form.bill_postal_code.data = customer_doc['address']['billing']['bill_postal_code']
        form.bill_country.data = customer_doc['address']['billing']['bill_country']
        form.ship_add1.data = customer_doc['address']['shipping']['ship_add1']
        form.ship_add2.data = customer_doc['address']['shipping']['ship_add2']
        form.ship_city.data = customer_doc['address']['shipping']['ship_city']
        form.ship_state.data = customer_doc['address']['shipping']['ship_state']
        form.ship_postal_code.data = customer_doc['address']['shipping']['ship_postal_code']
        form.ship_country.data = customer_doc['address']['shipping']['ship_country']

        text = "Edit Customer"
        action = url_for('customers.edit_customer', customer_id=customer_id)
        return render_template(
            'mod_customers/edit_customer.html',
            form=form,
            action=action,
            text=text
        )
    elif request.method == "POST":
        edit_costumers_document(customer_id)
        return redirect(url_for('customers.customers'))


@mod_customers.route('/delete/<customer_id>', methods=['GET'])
@login_required
def delete_customer(customer_id):
    mongo.db.customers.remove({'_id': ObjectId(customer_id)})

    return redirect(url_for('customers.customers'))


def build_customers_cursor(cursor):
    ''' Builds a JSON response for a given cursor
    '''
    response = json.loads('{}')
    response_to_append_to = response['results'] = []
    for idx, itm in enumerate(cursor):
        response_to_append_to.append(itm)
    return response


def build_save_costumers_document():

    customer_form = CustomerForm(request.form)
    costumer = customer_form.data

    json_obj = {}
    json_obj = {
        'company': {
            'name': costumer['company_name'],
            'slug': slugify(costumer['company_name'])
        },
        'first_name': {
            'value': costumer['first_name'],
            'slug': slugify(costumer['first_name']),
        },
        'last_name': {
            'value': costumer['last_name'],
            'slug': slugify(costumer['last_name'])
        },
        'customer_address': costumer['customer_address'],
        'job_title': costumer['job_title'],
        'phone': {
            'main_phone': costumer['main_phone'],
            'work_phone': costumer['work_phone'],
            'mobile': costumer['mobile'],
            'fax': costumer['fax'],
        },
        'address': {
            'billing': {
                'bill_add1': costumer['bill_add1'],
                'bill_add2': costumer['bill_add2'],
                'bill_city': costumer['bill_city'],
                'bill_state': costumer['bill_state'],
                'bill_postal_code': costumer['bill_postal_code'],
                'bill_country': costumer['bill_country'],
            },
            'shipping': {
                'ship_add1': costumer['ship_add1'],
                'ship_add2': costumer['ship_add2'],
                'ship_city': costumer['ship_city'],
                'ship_state': costumer['ship_state'],
                'ship_postal_code': costumer['ship_postal_code'],
                'ship_country': costumer['ship_country'],
            }
        },
        'email': costumer['email'],
        'website': costumer['website'],
        'provided_services': []
    }

    if current_user['region'] != "All":
        json_obj['region'] = current_user['region']
    else:
        json_obj['region'] = costumer['region']

    #municipality based on region
    #municipality based on region
    if costumer['municipality_region_north'] and costumer['region'] == "North":
        json_obj['municipality_region'] = costumer['municipality_region_north']

    if costumer['municipality_region_central'] and costumer['region'] == "Center":
        json_obj['municipality_region'] = costumer['municipality_region_central']

    if costumer['municipality_region_south'] and costumer['region'] == "South":
        json_obj['municipality_region'] = costumer['municipality_region_south']

    if costumer['municipality_region_west'] and costumer['region'] == "West":
        json_obj['municipality_region'] = costumer['municipality_region_west']

    if costumer['municipality_region_east'] and costumer['region'] == "East":
        json_obj['municipality_region'] = costumer['municipality_region_east']


    if costumer['customer_type'] == "Entrepreneur":
        json_obj['customer_type'] = {
            'target_group': costumer['customer_type'],
            'business_name': costumer['business_name'],
            'vat': costumer['vat'],
            'fiscal_number': costumer['fiscal_number'],
            'legal_entity_types': costumer['legal_entity_types'],
            'industry': costumer['industry'],
            'main_activity': costumer['main_activity'],
            'founding_year': costumer['founding_year'],
            'number_of_employees': costumer['number_of_employees'],
            'size_category': costumer['size_category'],
            'investment': costumer['investment'],
            'business_description': costumer['business_description']
        }
    elif costumer['customer_type'] == "Non-Governmental Organisation":
        json_obj['customer_type'] = {
            'target_group': costumer['customer_type'],
            'ngo_registration_number_ngo': costumer['ngo_registration_number_ngo'],
            'vat_number_ngo': costumer['vat_number_ngo'],
            'fiscal_number_ngo': costumer['fiscal_number_ngo'],
            'sector_ngo': costumer['sector_ngo'],
            'founding_year_ngo': costumer['founding_year_ngo'],
            'number_of_staff_ngo': costumer['number_of_staff_ngo'],
            'description_of_ngo': costumer['description_of_ngo'],
            'main_activities': costumer['main_activities'],
            'donors': costumer['donors']
        }
    elif costumer['customer_type'] == "Investor":
        json_obj['customer_type'] = {
            'target_group': costumer['customer_type'],
            'country': costumer['country'],
            'business': costumer['business'],
            'business_number': costumer['business_number'],
            'interest': costumer['interest'],
            'investor_industry': costumer['investor_industry'],
            'industry_of_interest': costumer['industry_of_interest'],
            'investor_size': costumer['investor_size'],
            'foundation_year_investor': costumer['foundation_year_investor'],
            'description_investor': costumer['description_investor']
        }
    else:
        json_obj['customer_type'] = {
            'target_group': costumer['customer_type'],
            'municipality_name': costumer['municipality_name'],
            'department': costumer['department'],
            'offering': costumer['offering'],
            'industries': costumer['industries'],
            'modules': costumer['modules'],
            'infrastructure_available': costumer['infrastructure_available'],
            'investment_incentives': costumer['investment_incentives'],
            'description': costumer['description']
        }
    mongo.db.customers.insert(json_obj)


def edit_costumers_document(customer_id):

    customer_form = CustomerForm(request.form)
    costumer = customer_form.data

    json_obj = {
        'company': {
            'name': costumer['company_name'],
            'slug': slugify(costumer['company_name'])
        },
        'first_name': {
            'value': costumer['first_name'],
            'slug': slugify(costumer['first_name']),
        },
        'last_name': {
            'value': costumer['last_name'],
            'slug': slugify(costumer['last_name'])
        },
        'customer_address': costumer['customer_address'],
        'job_title': costumer['job_title'],
        'phone': {
            'main_phone': costumer['main_phone'],
            'work_phone': costumer['work_phone'],
            'mobile': costumer['mobile'],
            'fax': costumer['fax'],
        },
        'address': {
            'billing': {
                'bill_add1': costumer['bill_add1'],
                'bill_add2': costumer['bill_add2'],
                'bill_city': costumer['bill_city'],
                'bill_state': costumer['bill_state'],
                'bill_postal_code': costumer['bill_postal_code'],
                'bill_country': costumer['bill_country'],
            },
            'shipping': {
                'ship_add1': costumer['ship_add1'],
                'ship_add2': costumer['ship_add2'],
                'ship_city': costumer['ship_city'],
                'ship_state': costumer['ship_state'],
                'ship_postal_code': costumer['ship_postal_code'],
                'ship_country': costumer['ship_country'],
            }
        },
        'email': costumer['email'],
        'website': costumer['website'],
    }

    if current_user['region'] != "All":
        json_obj['region'] = current_user['region']
    else:
        json_obj['region'] = costumer['region']

    #municipality based on region
    if costumer['municipality_region_north'] and costumer['region'] == "North":
        json_obj['municipality_region'] = costumer['municipality_region_north']

    if costumer['municipality_region_central'] and costumer['region'] == "Center":
        json_obj['municipality_region'] = costumer['municipality_region_central']

    if costumer['municipality_region_south'] and costumer['region'] == "South":
        json_obj['municipality_region'] = costumer['municipality_region_south']

    if costumer['municipality_region_west'] and costumer['region'] == "West":
        json_obj['municipality_region'] = costumer['municipality_region_west']

    if costumer['municipality_region_east'] and costumer['region'] == "East":
        json_obj['municipality_region'] = costumer['municipality_region_east']

    if costumer['customer_type'] == "Entrepreneur":
        json_obj['customer_type'] = {
            'target_group': costumer['customer_type'],
            'business_name': costumer['business_name'],
            'vat': costumer['vat'],
            'fiscal_number': costumer['fiscal_number'],
            'legal_entity_types': costumer['legal_entity_types'],
            'industry': costumer['industry'],
            'main_activity': costumer['main_activity'],
            'founding_year': costumer['founding_year'],
            'number_of_employees': costumer['number_of_employees'],
            'size_category': costumer['size_category'],
            'investment': costumer['investment'],
            'business_description': costumer['business_description']
        }
    elif costumer['customer_type'] == "Non-Governmental Organisation":
        json_obj['customer_type'] = {
            'target_group': costumer['customer_type'],
            'ngo_registration_number_ngo': costumer['ngo_registration_number_ngo'],
            'vat_number_ngo': costumer['vat_number_ngo'],
            'fiscal_number_ngo': costumer['fiscal_number_ngo'],
            'sector_ngo': costumer['sector_ngo'],
            'founding_year_ngo': costumer['founding_year_ngo'],
            'number_of_staff_ngo': costumer['number_of_staff_ngo'],
            'description_of_ngo': costumer['description_of_ngo'],
            'main_activities': costumer['main_activities'],
            'donors': costumer['donors']
        }
    elif costumer['customer_type'] == "Investor":
        json_obj['customer_type'] = {
            'target_group': costumer['customer_type'],
            'country': costumer['country'],
            'business': costumer['business'],
            'business_number': costumer['business_number'],
            'interest': costumer['interest'],
            'investor_industry': costumer['investor_industry'],
            'industry_of_interest': costumer['industry_of_interest'],
            'investor_size': costumer['investor_size'],
            'foundation_year_investor': costumer['foundation_year_investor'],
            'description_investor': costumer['description_investor']
        }
    else:
        json_obj['customer_type'] = {
            'target_group': costumer['customer_type'],
            'municipality_name': costumer['municipality_name'],
            'department': costumer['department'],
            'offering': costumer['offering'],
            'industries': costumer['industries'],
            'modules': costumer['modules'],
            'infrastructure_available': costumer['infrastructure_available'],
            'investment_incentives': costumer['investment_incentives'],
            'description': costumer['description']
        }

    mongo.db.customers.update(
        {'_id': ObjectId(customer_id)},
        {
            "$set": json_obj
        }
    )


def create_customer_report():
    fn = '%s/All Customers.xlsx' % current_app.config['EXCEL_DOC_DIR']

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


@mod_customers.route('/export-customers', methods=['POST', 'GET'])
@login_required
def export_customers():
    fn = create_customer_report()
    path = os.path.join(current_app.config['EXCEL_DOC_DIR'], fn)
    return send_file(path, mimetype='application/vnd.ms-excel')


@mod_customers.route('/reports')
@login_required
def reports():
    form = ServiceTypes()
    return render_template("mod_exports/exports.html", form=form)


def create_filtered_customer_report(response):
    fn = '%s/All Filtered Customers.xlsx' % current_app.config['EXCEL_DOC_DIR']

    workbook = xlsxwriter.Workbook(fn)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True, 'font_size': 7})
    font_size = workbook.add_format({'font_size': 7, 'align': 'center'})

    worksheet.set_column('A:A', 8)
    worksheet.set_column('B:B', 8)
    worksheet.set_column('C:C', 8)
    worksheet.set_column('D:D', 8)
    worksheet.set_column('E:E', 8)
    worksheet.set_column('F:F', 8)
    worksheet.set_column('G:G', 8)
    worksheet.set_column('H:H', 8)
    worksheet.set_column('I:I', 8)
    worksheet.set_column('J:J', 8)
    worksheet.set_column('K:K', 8)
    worksheet.set_column('L:L', 8)
    worksheet.set_column('M:M', 8)
    worksheet.set_column('N:N', 8)
    worksheet.set_column('O:O', 8)
    worksheet.set_column('P:P', 8)
    worksheet.set_column('Q:Q', 8)
    worksheet.set_column('R:R', 8)
    worksheet.set_column('S:S', 8)
    worksheet.set_column('T:T', 8)
    worksheet.set_column('U:U', 8)
    worksheet.set_column('V:V', 8)
    worksheet.set_column('W:W', 8)
    worksheet.set_column('X:X', 8)
    worksheet.set_column('Y:Y', 8)
    worksheet.set_column('Z:Z', 8)
    worksheet.set_column('AA:AA', 8)
    worksheet.set_column('AB:AB', 8)
    worksheet.set_column('AC:AC', 8)
    worksheet.set_column('AD:AD', 8)
    worksheet.set_column('AE:AE', 8)
    worksheet.set_column('AF:AF', 8)
    worksheet.set_column('AG:AG', 8)

    worksheet.write('A1', 'Client', bold)
    worksheet.write('B1', 'First Name', bold)
    worksheet.write('C1', 'Last Name', bold)
    worksheet.write('D1', 'Target Group', bold)
    worksheet.write('E1', 'Main Phone', bold)
    worksheet.write('F1', 'E-mail', bold)
    worksheet.write('G1', 'Website', bold)
    worksheet.write('H1', 'Region', bold)
    worksheet.write('I1', 'Main Activities', bold)
    worksheet.write('J1', 'Legal Entity Types', bold)
    worksheet.write('K1', 'Business Name', bold)
    worksheet.write('L1', 'Size Category', bold)
    worksheet.write('M1', 'No. of Employees', bold)
    worksheet.write('N1', 'Investment', bold)
    worksheet.write('O1', 'Industry', bold)
    worksheet.write('P1', 'Description', bold)
    worksheet.write('Q1', 'Founding Year', bold)
    worksheet.write('R1', 'Fiscal Number', bold)
    worksheet.write('S1', 'Sector', bold)
    worksheet.write('T1', 'Donors', bold)
    worksheet.write('U1', 'Sector', bold)
    worksheet.write('V1', 'Registration Number', bold)
    worksheet.write('W1', 'Interest', bold)
    worksheet.write('X1', 'Business Number', bold)
    worksheet.write('Y1', 'Industry of Interest', bold)
    worksheet.write('Z1', 'Investor Size', bold)
    worksheet.write('AA1', 'Country', bold)
    worksheet.write('AB1', 'Municipality Name', bold)
    worksheet.write('AC1', 'Investment Incentives', bold)
    worksheet.write('AD1', 'Offering', bold)
    worksheet.write('AE1', 'Department', bold)
    worksheet.write('AF1', 'Infrastructure Available', bold)
    worksheet.write('AG1', 'Modules', bold)

    i = 1
    for customer in response['results']:
        company = customer['company']['name']
        first_name = customer['first_name']['value']
        last_name = customer['last_name']['value']
        target_group = customer['customer_type']['target_group']
        phone = customer['phone']['main_phone']
        email = customer['email']
        website = customer['website']
        region = customer['region']

        worksheet.write(i, 0, company, font_size)
        worksheet.write(i, 1, first_name, font_size)
        worksheet.write(i, 2, last_name, font_size)
        worksheet.write(i, 3, target_group, font_size)
        worksheet.write(i, 4, phone, font_size)
        worksheet.write(i, 5, email, font_size)
        worksheet.write(i, 6, website, font_size)
        worksheet.write(i, 7, region, font_size)

        if target_group == "Entrepreneur":
            main_activity = customer['customer_type']['main_activity']
            legal_entity_types = customer['customer_type']['legal_entity_types']
            business_name = customer['customer_type']['business_name']
            size_category = customer['customer_type']['size_category']
            number_of_employees = customer['customer_type']['number_of_employees']
            investment = customer['customer_type']['investment']
            industry = customer['customer_type']['industry']
            business_description = customer['customer_type']['business_description']
            founding_year = customer['customer_type']['founding_year']
            fiscal_number = customer['customer_type']['fiscal_number']

            worksheet.write(i, 8, main_activity, font_size)
            worksheet.write(i, 9, legal_entity_types, font_size)
            worksheet.write(i, 10, business_name, font_size)
            worksheet.write(i, 11, size_category, font_size)
            worksheet.write(i, 12, number_of_employees, font_size)
            worksheet.write(i, 13, investment, font_size)
            worksheet.write(i, 14, industry, font_size)
            worksheet.write(i, 15, business_description, font_size)
            worksheet.write(i, 16, founding_year, font_size)
            worksheet.write(i, 17, fiscal_number, font_size)

        elif target_group == "Non-Governmental Organisation":
            number_of_staff_ngo = customer['customer_type']['number_of_staff_ngo']
            sector_ngo = customer['customer_type']['sector_ngo']
            founding_year_ngo = customer['customer_type']['founding_year_ngo']
            main_activities = customer['customer_type']['main_activities']
            fiscal_number_ngo = customer['customer_type']['fiscal_number_ngo']
            donors = customer['customer_type']['donors']
            description_of_ngo = customer['customer_type']['description_of_ngo']
            ngo_registration_number_ngo = customer['customer_type']['ngo_registration_number_ngo']

            worksheet.write(i, 8, main_activities, font_size)
            worksheet.write(i, 12, number_of_staff_ngo, font_size)
            worksheet.write(i, 15, description_of_ngo, font_size)
            worksheet.write(i, 16, founding_year_ngo, font_size)
            worksheet.write(i, 17, fiscal_number_ngo, font_size)
            worksheet.write(i, 19, donors, font_size)
            worksheet.write(i, 20, sector_ngo, font_size)
            worksheet.write(i, 21, ngo_registration_number_ngo, font_size)

        elif target_group == "Investor":
            investor_industry = customer['customer_type']['investor_industry']
            interest = customer['customer_type']['interest']
            foundation_year_investor = customer['customer_type']['foundation_year_investor']
            business_number = customer['customer_type']['business_number']
            business = customer['customer_type']['business']
            country = customer['customer_type']['country']
            description_investor = customer['customer_type']['description_investor']
            industry_of_interest = customer['customer_type']['industry_of_interest']
            investor_size = customer['customer_type']['investor_size']

            worksheet.write(i, 10, business, font_size)
            worksheet.write(i, 14, investor_industry, font_size)
            worksheet.write(i, 15, description_investor, font_size)
            worksheet.write(i, 16, foundation_year_investor, font_size)
            worksheet.write(i, 22, interest, font_size)
            worksheet.write(i, 23, business_number, font_size)
            worksheet.write(i, 24, industry_of_interest, font_size)
            worksheet.write(i, 25, investor_size, font_size)
            worksheet.write(i, 26, country, font_size)
        else:
            industries = customer['customer_type']['industries']
            investment_incentives = customer['customer_type']['investment_incentives']
            municipality_name = customer['customer_type']['municipality_name']
            description = customer['customer_type']['description']
            offering = customer['customer_type']['offering']
            department = customer['customer_type']['department']
            infrastructure_available = customer['customer_type']['infrastructure_available']
            modules = customer['customer_type']['modules']

            worksheet.write(i, 15, description, font_size)
            worksheet.write(i, 14, industries, font_size)
            worksheet.write(i, 27, municipality_name, font_size)
            worksheet.write(i, 28, investment_incentives, font_size)
            worksheet.write(i, 29, offering, font_size)
            worksheet.write(i, 30, department, font_size)
            worksheet.write(i, 31, infrastructure_available, font_size)
            worksheet.write(i, 32, modules, font_size)

        i = i + 1

    workbook.close()
    return fn


@mod_customers.route('/export-filtered-customers', methods=['GET'])
@login_required
def export_filtered_customers():
    if(len(request.args) > 0):
        customer = request.args.get('customer')
        target_group = request.args.get('target_group')
        region = request.args.get('region')

    query = {}

    if customer:
        query["company.slug"] = slugify(customer)

    if target_group:
        if target_group != "All":
            query["customer_type.target_group"] = target_group

    if region:
        if region != "All":
            query["region"] = region

    print query
    customers = mongo.db.customers.find(query)
    response = build_customers_cursor(customers)

    fn = create_filtered_customer_report(response)
    path = os.path.join(current_app.config['EXCEL_DOC_DIR'], fn)
    return send_file(path, mimetype='application/vnd.ms-excel')
