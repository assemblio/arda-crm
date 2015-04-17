from flask_wtf import Form
from wtforms import TextField, TextAreaField, SelectField


class SettingsForm(Form):

    site_title = TextField("Site Title")
    site_tagline = TextField("Site Subtitle")
    site_navbar_title = TextField("Site Navbar Title")
    web_url = TextField("Organization Website")
    fb_url = TextField("Facebook")
    tw_url = TextField("Twitter")
    li_url = TextField("LinkedIn")
    support_email = TextField('Supporting E-mail')

    region_opt = ['All', 'Center', 'East', 'West', 'North', 'South']
    region_options = SelectField(
        'Add to Region',
        choices=[
            (region, region) for region in region_opt[1:]
        ]
    )
    contactVia = TextField('Contacted Via')
    contactDescription = TextAreaField("Description")
