from flask import request, url_for, render_template, abort
from flask_api import FlaskAPI, status, exceptions
from flask_sqlalchemy import SQLAlchemy

import json
import subprocess
import os
import predictor

app = FlaskAPI(__name__)


@app.route('/')
def root():
    return render_template('index.html', available_symptoms=predictor.available_symptoms)


@app.route('/api/symptoms/all')
def available_symptoms():
    return predictor.available_symptoms


@app.route('/predict', methods=['POST'])
def foo():
    if not request.form:
        abort(400)

    result = predictor.predict(
        request.form['gender'], request.form['age'], request.form.getlist('symptoms'))
    return result

if __name__ == "__main__":
    context = ('ssl/machine.crt', 'ssl/machine.key')
    app.run(debug=True, ssl_context=context)
