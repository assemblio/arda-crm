from flask_wtf import Form
from wtforms import SelectField, TextField, RadioField


class CustomerForm(Form):

    customer = TextField("Customer")
    first_name = TextField("Costumer First Name")
    last_name = TextField("Costumer Last Name")
    email = TextField("E-mail")
    job_title = TextField("Job Title")
    phone_number = TextField("Phone Number")
    country = TextField("Country")
    city = TextField("City")
    address = TextField("Address")
    website = TextField("Website")
    target_group = SelectField(
        "Target Group",
        choices=[
            ('Entrepreneur', 'Entrepreneur'),
            ('Non-governmental organisation', 'Non-governmental organisation'),
            ('Investor', 'Investor'),
            ('Municipalitie', 'Municipalitie')
        ]
    )


    #if Target Group is Business/Entrepreneur
    business_name = TextField("Business Name")
    vat = RadioField("Vat")
    fiscal_number = TextField("Fiscal Number")
    legal_entity_types = TextField("Legal Entity Types")
    industry = TextField("industry")
    main_activity = TextField("Main Activity")
    founding_year = TextField("founding Year")
    number_of_employees = TextField("Number of Employees")
    size_category = SelectField("Size Category")
    investment = RadioField("Investment")
    business_description = TextField("Business Description")

    #if the Target Group is Municipality


    #if the Target Group is NGO
    ngo_registration_number_ngo = TextField("NGO Registration Number")
    vat_number_ngo = TextField("Vat Number NGO")
    fiscal_number_ngo = TextField("Fiscal Number NGO")
    sector_ngo = TextField("Sector NGO")
    founding_year_ngo = TextField("founding Year NGO")
    number_of_staff_ngo = TextField("Number of Staff NGO")
    description_of_ngo = TextField("Description of NGO")
    main_activities = TextField("Main Activities NGO")
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
