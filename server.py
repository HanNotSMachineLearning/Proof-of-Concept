from flask import request, render_template, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from predictor import Predictor


app = FlaskAPI(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/huisartsen'
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
        return '<Diagnose #%r: %r>' % (self.id, self.disease_id)


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
    return render_template('index.html', symptoms=availableSymptoms(), diseases=availableDiseases())


@app.route('/api/symptoms')
def availableSymptoms():
    return predictor.available_symptoms

@app.route('/api/diseases')
def availableDiseases():
    return predictor.ziektes

@app.route('/predict', methods=['POST'])
def predict():
    if not request.form:
        abort(400)
    symptoms_input = request.form.getlist('symptoms') 
    result = predictor.predict(request.form['gender'], request.form['age'], symptoms_input)
    gender_bool = request.form['gender'] == "1"

    gender = 'man' if gender_bool else 'vrouw'

    for r in result:
        r['chance'] = round(float(r['chance'])*100, 2)

    return render_template('result.html',prediction=result,gender=gender,gender_bool=int(gender_bool),age=request.form['age'],symptoms=symptoms_input)

@app.route('/diagnosis', methods=['POST'])
def addDiagnosis():
    data = request.get_json()
    diagnose = Diagnose(gender=bool(data['gender']), age=data['age'], disease_id=Disease.query.filter_by(name=data['disease']).first().id)
    for symptom in data['symptoms']:
        diagnose.symptoms.append(Symptom.query.filter_by(name=symptom).first())

    db.session.add(diagnose)
    db.session.commit()
    return "done"
    

if __name__ == "__main__":
    context = ('ssl/machine.crt', 'ssl/machine.key')
    app.run(debug=True, ssl_context=context)
