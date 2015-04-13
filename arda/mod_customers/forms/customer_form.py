# -*- coding: UTF-8 -*-
from flask_wtf import Form
from wtforms import SelectField, TextField, RadioField, HiddenField, TextAreaField


class CustomerForm(Form):

    municipalities = [
        'All', 'Prishtine', 'Drenas', 'Fushe Kosove', 'Obilliq', 'Podujeve',
        'Shtime', 'Gracanice', 'Lipjan',
        'All', 'Vushtrri', 'Zubin Potok', 'Zvecan', 'Leposavic', ' Mitrovice', 'Skenderaj',
        'All', 'Istog', 'Kline', ' Peja', 'Junik', 'Decan', 'Gjakova',
        'All', 'Prizren', 'Malisheva', 'Suhareka', 'Dragash', 'Mamusha', 'Rahovec',
        'All', 'Ferizaj', 'Gjilan', 'Viti', 'Novoberde', 'Kamenice', 'Hani Elezit', 'Kacanik',
        'Shterpce', 'Ranillug', 'Kllokot', 'Partesh'
    ]

    municipality = SelectField('Municipality', choices=[(x, x) for x in municipalities])
    municipality_region_central = SelectField('Municipality', choices=[(x, x) for x in municipalities[1:9]])
    municipality_region_north = SelectField('Municipality', choices=[(x, x) for x in municipalities[10:16]])
    municipality_region_west = SelectField('Municipality', choices=[(x, x) for x in municipalities[17:23]])
    municipality_region_south = SelectField('Municipality', choices=[(x, x) for x in municipalities[24:30]])
    municipality_region_east = SelectField('Municipality', choices=[(x, x) for x in municipalities[31:42]])

    search_municipality_region_central = SelectField('Municipality', choices=[(x, x) for x in municipalities[0:9]])
    search_municipality_region_north = SelectField('Municipality', choices=[(x, x) for x in municipalities[9:16]])
    search_municipality_region_west = SelectField('Municipality', choices=[(x, x) for x in municipalities[16:23]])
    search_municipality_region_south = SelectField('Municipality', choices=[(x, x) for x in municipalities[23:30]])
    search_municipality_region_east = SelectField('Municipality', choices=[(x, x) for x in municipalities[30:42]])

    arda_regions = ['North', 'East', 'West', 'South', 'Center']
    choices = [(x, x) for x in arda_regions]
    region = SelectField("Region", choices=choices)

    company_name = TextField("Customer")
    first_name = TextField("First Name")
    last_name = TextField("Last Name")
    job_title = TextField("Job Title")
    main_phone = TextField("Main Phone")
    work_phone = TextField("Work Phone")
    mobile = TextField("Mobile Phone")
    fax = TextField("Fax")
    email = TextField("E-mail")
    website = TextField("Website")
    customer_address = TextAreaField('Adderess')
    customer_type = SelectField(
        "Customer Type",
        choices=[
            ('Business/Entrepreneur', 'Business/Entrepreneur'),
            ('Non-Governmental Organisation', 'Non-Governmental Organisation'),
            ('Investor', 'Investor'),
            ('Municipality', 'Municipality')
        ]
    )

    #if Target Group is Business/Entrepreneur
    business_name = TextField("Business Name")
    vat = TextField("VAT Number")
    business_number = TextField("Business Number")
    fiscal_number = TextField("Fiscal Number")
    legal_entity_types = TextField("Legal Entity Type")
    industry = TextField("Industry")
    main_activity = TextAreaField(" Business Dectription/Main Activity")
    founding_year = TextField("Founding Year")
    number_of_employees = TextField("Number of Employees")
    size_category = SelectField(
        "Size",
        choices=[
            ('Micro', 'Micro (1-9)'),
            ('Small', 'Small (10-49)'),
            ('Medium', 'Medium (50-249)'),
            ('Large', 'Large (250+)')
        ]
    )
    search_size_category = SelectField(
        "Size",
        choices=[
            ('All', 'All'),
            ('Micro', 'Micro (1-9)'),
            ('Small', 'Small (10-49)'),
            ('Medium', 'Medium (50-249)'),
            ('Large', 'Large (250+)')
        ]
    )
    investment = RadioField(
        "Interested in Invesment",
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
        ]
    )
    business_description = TextAreaField("Primary Interest for Cooperation")

    #Target Group: Investor
    country = TextField("Country")
    business = TextField("Business")
    investor_business_number = TextField("Business Number")
    investor_vat = TextField("VAT Number")
    investor_fiscal_number = TextField("Fiscal Number")
    interest = TextField("Interest")
    investor_industry = TextField("Industry")
    industry_of_interest = TextField("Industry of interest")
    investor_size = TextField("Size")
    foundation_year_investor = TextField("Foundation Year")
    description_investor = TextAreaField("Business Description")

    department_choices = [
        'Department of Finance',
        'Department for Economic Development',
        'Department for Education',
        'Department for Health',
        'Department for Culture and Sport',
        'Department for Infrastructure',
        'Department for Public Services',
        'General Department of Cadaster',
        'Department of Administration',
        'Department of Inspections',
        'Department of Agriculture'
    ]
    #Target Group: Municipality
    municipality_name = TextField("Municipality Name")
    department = SelectField("Department", choices=[(x, x) for x in department_choices])
    offering = TextField("Offering")
    industries = TextField("Industries")
    modules = TextField("Modules")
    infrastructure_available = TextField("Infrastructure Available")
    investment_incentives = TextField("Investment Incentives")
    description = TextAreaField("Description")

    #if the Target Group is NGO
    ngo_registration_number_ngo = TextField("Registration Number")
    vat_number_ngo = TextField("VAT Number")
    fiscal_number_ngo = TextField("Fiscal Number")
    sector_ngo = TextField("Sector")
    founding_year_ngo = TextField("Founding Year")
    number_of_staff_ngo = TextField("Number of Staff")
    description_of_ngo = TextAreaField("Description")
    main_activities = TextField("Main Activities")
    donors = TextField("Donors")

    #Bill to Address fields
    bill_add1 = TextField("Invoice/Bill To Address:")
    bill_add2 = TextField("Invoice/Bill To Address ")
    bill_city = TextField("City")
    bill_state = TextField("State")
    bill_postal_code = TextField("Postal code")
    bill_country = TextField("Country")
    #Ship to Address fields
    ship_add1 = TextField("Ship to Address:")
    ship_add2 = TextField("Ship to Address")
    ship_city = TextField("City")
    ship_state = TextField("State")
    ship_postal_code = TextField("Postal code")
    ship_country = TextField("Country")
