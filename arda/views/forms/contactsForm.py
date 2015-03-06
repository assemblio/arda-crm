from flask_wtf import Form
from wtforms import SelectField, TextField

class ContactsForm(Form):

    job_type = SelectField("Job type", choices=[('Municipality', 'Municipality')])