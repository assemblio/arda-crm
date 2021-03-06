from flask_wtf import Form
from wtforms import RadioField, TextField, PasswordField, SelectField


class UserForm(Form):

    arda_regions = ['All', 'North', 'East', 'West', 'South', 'Center']
    choices = [(x, x) for x in arda_regions]

    region = SelectField("Region", choices=choices)
    region_regular = SelectField("Region", choices=choices[1:])
    first_name = TextField("First Name")
    last_name = TextField("Last Name")
    email = TextField("E-mail")
    password = PasswordField("Password")
    role = RadioField(
        "User Privilege",
        choices=[
            ('Regular', 'Regular'),
            ('Admin', 'Admin'),
        ],
        default='Regular'
    )
