from flask_wtf import Form
from wtforms import TextField

class ThemeForm(Form):

    landingpage_banner_image_url = TextField("Banner Image URL")