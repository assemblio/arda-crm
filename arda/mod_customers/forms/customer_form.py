from flask_wtf import Form
from wtforms import SelectField, TextField


class CustomerForm(Form):

    company_name = TextField("Company Name")
    first_name = TextField("Costumer First Name")
    last_name = TextField("Costumer Last Name")
    job_title = TextField("Job Title")
    main_phone = TextField("Main Phone")
    work_phone = TextField("Work Phone")
    mobile = TextField("Mobile")
    fax = TextField("Fax")
    email = TextField("E-mail")
    website = TextField("Website")
    costumer_type = SelectField(
        "Costumer Type",
        choices=[
            ('Entrepreneur', 'Entrepreneur'),
            ('Non-governmental organisation', 'Non-governmental organisation'),
            ('Investor', 'Investor'),
            ('Municipalitie', 'Municipalitie')
        ]
    )

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
