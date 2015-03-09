from flask_wtf import Form
from wtforms import SelectField, TextField, TextAreaField


class ContactsForm(Form):

    company_name = TextField("Company Name")
    full_name = TextField("Costumer Full Name")
    job_title = TextField("Job Title")
    main_phone = TextField("Main Phone")
    work_phone = TextField("Work Phone")
    mobile = TextField("Mobile")
    fax = TextField("Fax")
    email = TextField("E-mail")
    website = TextField("Website")
    bill_address = TextAreaField("Invoice/Bill To")
    ship_address = TextAreaField("Ship to")
    costumer_type = SelectField(
        "Costumer Type",
        choices=[
            ('Municipality', 'Municipality'),
            ('Business', 'Business'),
            ('Investor', 'Investorss')
        ]
    )
