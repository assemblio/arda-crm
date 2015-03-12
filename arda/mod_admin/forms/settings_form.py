from flask_wtf import Form
from wtforms import TextField

class SettingsForm(Form):

    site_title = TextField("Site Title")
    site_tagline = TextField("Site Subtitle")