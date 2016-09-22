#!flask/bin/python
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class UrlForm(Form):
    submission_url = StringField('submission_url', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
