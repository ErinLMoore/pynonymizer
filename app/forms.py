#!flask/bin/python
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import URL

class UrlForm(Form):
    submission_url = StringField('submission_url', validators=[URL()])
    description = StringField('description', validators=[DataRequired()])
