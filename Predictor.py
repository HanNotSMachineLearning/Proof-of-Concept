from sklearn.ensemble import RandomForestClassifier

class Predictor(object):

    def __init__(self, available_symptoms, diseases, features, labels):
        """Constructor van de Predictor klasse.

        Args:
            available_symptoms: alle symptomen die ingevuld kunnen worden door de gebruiker.
            diseases: de ziekten die voorspeld kunnen worden.
            features: alle features die het model moet leren.
            labels: alle labels die het model moet leren. Het aantal labels moet gelijk zijn aan de aantal rijen voor de features.
        """
        self.available_symptoms = available_symptoms
        self.diseases = diseases
        self.alg = RandomForestClassifier(n_estimators=50, random_state=0)
        self.clf = self.alg.fit(features, labels)
        
    def predict(self, gender, age, symptoms):
        """Functie om het model te gebruiken om de meest relevante ziekten te voorspellen.

        Args:
            gender: het geslacht van de gebruiker. 0 staat voor vrouw, 1 staat voor man.
            age: de leeftijd van de gebruiker.
            symptoms: de symptomen van de gebruiker.
        
        Returns:
            Een gesorteerde array van objecten waarbij elk object een ziekte is met de volgende twee keys:
            disease: de naam van de ziekte.
            chance: de kans dat deze ziekte het meest relevant is.
        
        Raises:
            Exception: als er symptomen ingevoerd zijn waar de instantie geen kennis over beschikt. 
        """
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
        return sorted([{'chance': x, 'disease': self.ziektes[i]} for i,x in enumerate(predictions)], key=lambda x: x['chance'], reverse=True)[:3]

