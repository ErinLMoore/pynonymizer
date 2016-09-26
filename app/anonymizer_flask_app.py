#!flask/bin/python3

from flask import Flask
from flask import jsonify
from flask import render_template

from .forms import UrlForm
from .anonymizer import Anonymizer
from app import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    user = {'name': 'test'}  # fake user
    form = UrlForm()
    if form.validate_on_submit():
        form_dict ={"url": form.submission_url.data, "description": form.description.data}
        anonymizer = Anonymizer(form_dict['url'], form_dict['description'])
        anonymizer.anonymize()
        result = anonymizer.get_result()
        return render_template('result.html',
                                result=result)
    return render_template('index.html',
                           form=form,)

@app.route('/result', methods=['GET', 'PUT'])
def result():
    return render_template('result.html',
                            result = RESULT)
