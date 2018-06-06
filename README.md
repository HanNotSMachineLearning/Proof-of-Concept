# Proof-of-Concept

## Functionaliteit

Dit proof-of-concept dient als prototype voor een toekomstige applicatie om huisartsen te assisteren met het maken van correcte diagnosen voor haar patiënten en specialisten. Dit proof-of-concept heeft nog niet alle criteria die beschreven zijn in het onderzoeksrapport in deelvraag 2.

De criteria die geraakt zijn met dit proof-of-concept zijn als volgt:

- Het systeem geeft aan de hand van de ingevoerde symptomen resultaten terug, gesorteerd op relevantie.
- Het systeem mag geen gegevens van patiënten bewaren.
- Het systeem moet zelflerend zijn
- Het systeem moet minimaal 95% van de tijd toegankelijk zijn.
- Het systeem moet binnen vijftien seconden met een resultaat komen.
- De applicatie moet een web- of desktopapplicatie worden.
- Het systeem mag geen gegevens van patiënten bewaren.
- Het systeem accepteert alleen text-based input.

De criteria waarin dit proof-of-concept **NIET** voldoet zijn als volgt:

- De gebruiker moet in staat zijn symptomen tekstueel in te voeren in het systeem.
- Het systeem accepteert alleen text-based input.
- Het systeem geeft de gebruiker toegang tot de applicatie doordat deze correcte inloggegevens invoert. 
- Het moet mogelijk zijn om nieuwe symptomen en ziekten in te voeren in de applicatie.
- De gebruiker is in staat het systeem feedback te geven op het gegeven resultaat.

## Installeren van de afhankelijkheden

1. Installeer [Python 3.6.5](https://www.python.org/downloads/release/python-365/).
2. Ga in een terminal-venster naar de map waar het proof-of-concept staat.
3. Gebruik het commando `pip install -r requirements.txt --user` om de Python-modulen te installeren.
4. Installeer [MySQL Community Server 8.0.11](https://dev.mysql.com/downloads/mysql/). Hiervoor wordt er mogelijk gevraagd om een account aan te maken om uw server te beveiligen.

## Opstarten van het proof-of-concept

1. Start uw MySQL-server op.
2. Zorg ervoor dat u een database gecreëerd heeft genaamd '`huisartsen`'.
3. Importeer het bestand '`dump.sql`' in uw database die u in de vorige stap aangemaakt hebt.
4. Zorg ervoor op regel 10 van het bestand '`server.py`' dat de goede database-gegevens ingevuld zijn.
5. Ga in een terminal-venster naar de map waar het proof-of-concept staat.
6. Start het proof-of-concept met het commando `python server.py`.
7. Ga met uw browser naar https://localhost:5000.

U draait nu de applicatie en u kunt predicties uitvoeren.

## Structuur / klassen

### Algemeen

In de `server` module wordt de webserver gestart die gebruik maakt van `Flask`. Met `Flask` worden drie REST-endpoints gecreëerd: eentje voor het serveren van de index-pagina (`GET /`), een voor het indienen van een verzoek om een predictie te doen (`POST /predict`) en een voor het ophalen van alle symptomen die geregistreerd staan in de database (`GET /api/symptoms/all`).

Verder heeft deze webserver toegang tot een (remote) database via `SQLAlchemy`, wat nodig is om de symptomen, ziekten en diagnosen uit te lezen uit de database. Deze data wordt doorgegeven aan het algoritme waarna er predicties uitgeoefend kunnen worden, wat in dit geval de verantwoordelijkheid is van de `Predictor`-klasse. 

### Predictor

De berekeningen die de meest relevante ziekten retourneren worden gedaan in de `Predictor`-klasse. Je kan per instantie van de `Predictor`-klasse aangeven welke ziekten en symptomen er zijn, en zo kan je meerdere modellen creëren voor verschillende datasets.

Er zijn twee functies in deze klasse:

```python
def __init__(self, available_symptoms, diseases, features, labels):
  """Constructor van de Predictor klasse.

  Args:
    available_symptoms: alle symptomen die ingevuld kunnen worden door de gebruiker.
    diseases: de ziekten die voorspeld kunnen worden.
    features: alle features die het model moet leren.
    labels: alle labels die het model moet leren. Het aantal labels moet gelijk zijn aan de aantal rijen voor de features.
  """
```

```python
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
```