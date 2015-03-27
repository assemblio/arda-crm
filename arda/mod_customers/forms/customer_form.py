from flask_wtf import Form
from wtforms import SelectField, TextField, RadioField, HiddenField, TextAreaField


class CustomerForm(Form):

    municipalities = [
        'Deqan', 'Gjakove', 'Gllogoc', 'Gjilan', 'Dragash', 'Istog', 'Kaqanik',
        'Kline', 'Fushe Kosove', 'Kamenice', 'Mitrovice', 'Leposaviq', 'Lipjan',
        'Novoberde', 'Obilic', 'Rahovec', 'Peje', 'Podujeve', 'Prizren', 'Skenderaj',
        'Shtime', 'Shterpce', 'Suhareke', 'Ferizaj', 'Viti', 'Vushtrri', 'Zubin Potok',
        'Zveqan', 'Malisheve', 'Hani i Elezit', 'Mamushe', 'Junik', 'Prishtina',
        'Kllokoti', 'Graqanice', 'Ranillug', 'Partesh', ' Mitrovica Veriore',
    ]

    municipality = SelectField('Choose Municipality', choices=[(x, x) for x in municipalities[0:11]])

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
            ('All', 'All'),
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

    #if the Target Group is Municipality


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