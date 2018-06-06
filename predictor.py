from sklearn.ensemble import RandomForestClassifier

class Predictor(object):

    def __init__(self, available_symptoms, ziektes, features, labels):
        self.available_symptoms = available_symptoms
        self.ziektes = ziektes

        # create a decision tree classifier
        self.alg = RandomForestClassifier(n_estimators=50, random_state=0)
        self.clf = self.alg.fit(features, labels)

    def predict(self, gender, age, symptoms):
        gender = bool(gender)
        age = int(age)

        existing_symptoms = list(filter(lambda v: v in self.available_symptoms, symptoms))

        if len(existing_symptoms) != len(symptoms):
            not_existing_symptoms = list(
                set(symptoms) - set(existing_symptoms))
            raise Exception("U mag alleen symptomen opnoemen die bij ons geregistreerd zijn. De symptomen die u invulde maar niet bij ons geregistreerd staan zijn: " + ",".join(not_existing_symptoms))

        symptoms_array = [gender, age]

        for available_symptom in self.available_symptoms:
            symptoms_array.append(1 if available_symptom in symptoms else 0)

        predictions = self.clf.predict_proba([symptoms_array])[0]

        value, index = max([(v, i) for i, v in enumerate(predictions)])

        return {
            'disease': self.ziektes[index],
            'chance': value
        }
