
from website.models import Temperature, Humidity
from website import db

def addTemperature(temp):
    db.session.add(Temperature(temperature=temp))
    db.session.commit()

def addHumidity(humid):
    db.session.add(Humidity(humidity=humid))
    db.session.commit()
