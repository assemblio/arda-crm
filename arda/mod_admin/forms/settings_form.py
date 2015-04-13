from flask_wtf import Form
from wtforms import TextField


class SettingsForm(Form):

    site_title = TextField("Site Title")
    site_tagline = TextField("Site Subtitle")
    site_navbar_title = TextField("Site Navbar Title")
    web_url = TextField("Organization Website")
    fb_url = TextField("Facebook")
    tw_url = TextField("Twitter")
    li_url = TextField("LinkedIn")
    support_email = TextField('Supporting E-mail')
