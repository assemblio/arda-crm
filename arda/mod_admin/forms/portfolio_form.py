from flask_wtf import Form
from wtforms import TextField, TextAreaField

class PortfolioForm(Form):

    title = TextField("Title")
    subtitle = TextField("Subtitle")
    image_url = TextField("Image URL")
    description = TextAreaField("Description")