from flask import request, render_template, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

import predictor

app = FlaskAPI(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:koekje@localhost/huisartsen'
db = SQLAlchemy(app)

# Database

diagnose_symptoms = db.Table('diagnose_symptoms', db.Column('diagnose_id', db.Integer, db.ForeignKey(
    'diagnose.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False), db.Column('symptom_id', db.Integer, db.ForeignKey('symptom.id',  ondelete='CASCADE', onupdate='CASCADE'), nullable=False))


class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Diagnose(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Boolean, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    symptoms = db.relationship('Symptom', secondary=diagnose_symptoms, lazy='subquery',
                               backref=db.backref('diagnoses', lazy=True))

    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id', ondelete='CASCADE', onupdate='CASCADE'),
                           nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

db.create_all()


import csv
# Add diseases
astma = Disease(id=1, name='Astma')
bronchitis = Disease(id=2, name='Bronchitis')
griep = Disease(id=3, name='Griep')
longontsteking = Disease(id=4, name='Longontsteking')
verkoudheid = Disease(id=5, name='Verkoudheid')

db.session.merge(astma)
db.session.merge(bronchitis)
db.session.merge(griep)
db.session.merge(longontsteking)
db.session.merge(verkoudheid)

db.session.commit()


with open('Data/Dataset-100.csv', newline='') as csvfile:

    # db.session.execute('''TRUNCATE TABLE diagnose''')
    # db.session.commit()

    rows = list(csv.reader(csvfile))
    print(rows[0][1:5])
    for i, header in enumerate(rows[0][2:-1]):
        print("Header rij")
        print(header)

        symptom = Symptom(id=i + 1, name=header)
        db.session.merge(symptom)

    db.session.commit()

    for i, row in enumerate(rows[1:]):
        print("Rij")
        me = Diagnose(id=i + 1, gender=bool(
            int(row[0])), age=row[1], disease_id=str(int(row[-1]) + 1))
        for symptom_id, symptom in enumerate(row[2:-1]):
            if symptom == '1':
                me.symptoms.append(Symptom.query.get(symptom_id + 1))

        db.session.merge(me)

    db.session.commit()


# Flask
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
