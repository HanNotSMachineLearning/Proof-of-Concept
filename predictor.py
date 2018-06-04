#!/usr/bin/env python3

import sys
import csv
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# read csv files
available_symptoms = []
with open('Data/Dataset-100.csv', 'r') as DataFile:
    train_data = list(csv.reader(DataFile))
    available_symptoms = list(
        map(lambda v: v.strip().lower(), train_data[0]))[2:-1]
    train_data = train_data[1:]

# datasets
features = []
labels = []

ziektes = ['Astma', 'Bronchitis', 'Griep', 'Longontsteking', 'Verkoudheid']

# split labels from features
for item in train_data:
    item = list(map(lambda v: int(v), item))
    labels.append(item[-1])
    features.append(item[:-1].copy())

# create a decision tree classifier
clf = RandomForestClassifier(n_estimators=50, random_state=0)
# train the classifier with the trainingsdata
clf = clf.fit(features, labels)


def predict(gender, age, symptoms):
    gender = bool(gender)
    age = int(age)

    existing_symptoms = list(
        filter(lambda v: v in available_symptoms, symptoms))

    if len(existing_symptoms) != len(symptoms):
        not_existing_symptoms = list(
            set(symptoms) - set(existing_symptoms))
        raise Exception(
            "U mag alleen symptomen opnoemen die bij ons geregistreerd zijn. De symptomen die u invulde maar niet bij ons geregistreerd staan zijn: " + ",".join(not_existing_symptoms))

    symptoms_array = [gender, age]
    for available_symptom in available_symptoms:
        symptoms_array.append(1 if available_symptom in symptoms else 0)

    predictions = clf.predict_proba([symptoms_array])[0]
    value, index = max([(v, i) for i, v in enumerate(predictions)])

    return {
        'disease': ziektes[index],
        'chance': value
    }
