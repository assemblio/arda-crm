from flask_wtf import Form
from wtforms import RadioField, TextField, PasswordField


class UserForm(Form):

    first_name = TextField("First Name")
    last_name = TextField("Last Name")
    email = TextField("E-mail")
    password = PasswordField("Password")
    role = RadioField(
        "User Type",
        choices=[
            ('Regular', 'regular'),
            ('Admin', 'admin')
        ],
        default='Regular'
    )
