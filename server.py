from flask import request, url_for, render_template, abort
from flask_api import FlaskAPI, status, exceptions
import json

app = FlaskAPI(__name__)

available_symptoms = ('test', 'skrt')


@app.route('/')
def root():
    return render_template('index.html', available_symptoms=available_symptoms)


@app.route('/foo', methods=['POST'])
def foo():
    if not request.form:
        abort(400)

    print(request.form.getlist('symptoms'))
    return json.dumps(request.form)

if __name__ == "__main__":
    app.run(debug=True)
