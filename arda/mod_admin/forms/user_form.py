from flask_wtf import Form
from wtforms import RadioField, TextField


class UserForm(Form):

    first_name = TextField("First Name")
    last_name = TextField("Last Name")
    email = TextField("E-mail")
    password = TextField("Password")
    role = RadioField(
        "User Type",
        choices=[
            ('Regular', 'regular'),
            ('Admin', 'admin')
        ],
        default='regular'
    )
