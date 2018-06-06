from flask import request, render_template, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from predictor import Predictor


app = FlaskAPI(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://poc:Test123!@localhost/huisartsen'
db = SQLAlchemy(app)

# Database
diagnose_symptoms = db.Table('diagnose_symptoms', db.Column('diagnose_id', db.Integer, db.ForeignKey(
    'diagnose.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False), db.Column('symptom_id', db.Integer, db.ForeignKey('symptom.id',  ondelete='CASCADE', onupdate='CASCADE'), nullable=False))


class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Disease %r>' % self.name


class Diagnose(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Boolean, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    symptoms = db.relationship('Symptom', secondary=diagnose_symptoms, lazy='subquery',
                               backref=db.backref('diagnoses', lazy=True))

    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id', ondelete='CASCADE', onupdate='CASCADE'),
                           nullable=False)

    def __repr__(self):
        return '<Diagnose %r>' % self.id


class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Symptom %r>' % self.name

db.create_all()


available_symptoms = list(map(lambda x: x.name, Symptom.query.all()))
diseases = list(map(lambda x: x.name, Disease.query.all()))
diagnoses = Diagnose.query.all()
features = []
for diagnose in diagnoses:
    symptoms = [0] * len(available_symptoms)
    for symptom in diagnose.symptoms:
        symptoms[symptom.id - 1] = 1
    feature = [int(diagnose.gender), diagnose.age] + symptoms
    features.append(feature)

labels = list(map(lambda v: int(v.disease_id) - 1, diagnoses))

predictor = Predictor(available_symptoms, diseases, features, labels)
# Flask


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
