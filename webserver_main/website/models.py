from . import db
from sqlalchemy.sql import func
from sqlalchemy import Numeric

class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(Numeric(precision=5, scale=2))  # Precision: 5, Scale: 2 (two decimal places)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
        
class Humidity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    humidity = db.Column(Numeric(precision=5, scale=2))    
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    