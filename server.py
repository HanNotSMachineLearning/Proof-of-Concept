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
    return render_template('index.html')


@app.route('/api/symptoms')
def available_symptoms():
    return predictor.available_symptoms

@app.route('/api/diseases')
def available_duseases():
    return predictor.ziektes


@app.route('/predict', methods=['POST'])
def foo():
    if not request.form:
        abort(400)
    result = predictor.predict(
        request.form['gender'], request.form['age'], request.form.getlist('symptoms'))
    gender = 'man'
    if request.form['gender'] == 0:
        gender = 'vrouw'
    return render_template('result.html',disease=result['disease'],accuracy=round(float(result['chance'])*100, 2),gender=gender,age=request.form['age'],symptoms=request.form.getlist('symptoms'))


if __name__ == "__main__":
    context = ('ssl/machine.crt', 'ssl/machine.key')
    app.run(debug=True, ssl_context=context)
