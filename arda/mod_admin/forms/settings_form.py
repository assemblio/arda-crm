from flask_wtf import Form
from wtforms import TextField

class SettingsForm(Form):

    site_title = TextField("Site Title")
    site_tagline = TextField("Site Subtitle")
    site_navbar_title = TextField("Site Navbar Title")
    landingpage_banner_image_url = TextField("Banner Image URL")