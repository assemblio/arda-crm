# -*- coding: UTF-8 -*-
from flask_wtf import Form
from wtforms import SelectField, TextField, RadioField, HiddenField, TextAreaField


class CustomerForm(Form):

    municipalities = [
    	'Prishtine', 'Drenas', 'Fushe Kosove', 'Obilliq', 'Podujeve',
    	'Shtime', 'Gracanice', 'Lipjan',
    	'Vushtrri', 'Leposavic', ' Mitrovice', 'Skenderaj',
    	'Istog', 'Kline',' Peja', 'Junik', 'Decan', 'Gjakova',
    	'Prizren', 'Dragash', 'Suhareka', 'Dragash', 'Mamusha', 'Rahovec',
        'Ferizaj', 'Gjilan', 'Viti', 'Novoberde', 'Kamenice', 'Hani Elezit', 'Kacanik',
        'Shterpce', 'Ranillug', 'Kllokot', 'Partesh'
    ]

    municipality = SelectField('Choose Municipality', choices=[(x, x) for x in municipalities])
    municipality_region_central = SelectField('Choose Municipality', choices=[(x, x) for x in municipalities[0:8]])
    municipality_region_north = SelectField('Choose Municipality', choices=[(x, x) for x in municipalities[8:12]])
    municipality_region_west = SelectField('Choose Municipality', choices=[(x, x) for x in municipalities[12:18]])
    municipality_region_south = SelectField('Choose Municipality', choices=[(x, x) for x in municipalities[18:24]])
    municipality_region_east = SelectField('Choose Municipality', choices=[(x, x) for x in municipalities[24:34]])

    arda_regions = ['North', 'East', 'West', 'South', 'Center']
    choices = [(x, x) for x in arda_regions]

    region = SelectField("Region", choices=choices)

    company_name = TextField("Customer")
    first_name = TextField("Costumer First Name")
    last_name = TextField("Costumer Last Name")
    job_title = TextField("Job Title")
    main_phone = TextField("Main Phone")
    work_phone = TextField("Work Phone")
    mobile = TextField("Mobile Phone")
    fax = TextField("Fax")
    email = TextField("Email")
    website = TextField("Website")
    customer_address = TextAreaField('Customer Adderess')
    customer_type = SelectField(
        "Costumer Type",
        choices=[
            ('Entrepreneur', 'Entrepreneur'),
            ('Non-Governmental Organisation', 'Non-Governmental Organisation'),
            ('Investor', 'Investor'),
            ('Municipality', 'Municipality')
        ]
    )


    #if Target Group is Business/Entrepreneur
    business_name = TextField("Business Name")
    vat = RadioField(
        "VAT Number",
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
        ],
        default='Yes'
    )
    fiscal_number = TextField("Fiscal Number")
    legal_entity_types = TextField("Legal Entity Types")
    industry = TextField("Industry")
    main_activity = TextField("Main Activity")
    founding_year = TextField("Founding Year")
    number_of_employees = TextField("Number of Employees")
    size_category = SelectField(
        "Size",
        choices=[
            ('Micro', 'Micro'),
            ('Small', 'Small'),
            ('Medium', 'Medium'),
            ('Large', 'Large')
         ]
     )
    investment = RadioField(
        "Investment",
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
        ],
        default='Yes'
    )
    business_description = TextAreaField("Business Description")

    #Target Group: Investor
    country = TextField("Country")
    business = TextField("Business")
    business_number = TextField("Business Number")
    interest = TextField("Interest")
    investor_industry = TextField("Industry")
    industry_of_interest = TextField("Industry of interest")
    investor_size = TextField("Size")
    foundation_year_investor = TextField("Foundation year")
    description_investor = TextField("Description of Business")

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
    infrastructure_available = TextField("Infrastructure available")
    investment_incentives = TextField("Investment Incentives")
    description = TextField("Description")

    #if the Target Group is NGO
    ngo_registration_number_ngo = TextField("Registration Number")
    vat_number_ngo = TextField("VAT Number")
    fiscal_number_ngo = TextField("Fiscal Number")
    sector_ngo = TextField("Sector")
    founding_year_ngo = TextField("Founding Year")
    number_of_staff_ngo = TextField("Number of Staff")
    description_of_ngo = TextAreaField("Description")
    main_activities = TextField("Main Activities")
    web_site = TextField("Web Site")
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

    target_group = HiddenField()