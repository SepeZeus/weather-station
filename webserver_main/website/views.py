from flask import Blueprint, render_template, request, flash, jsonify
from .models import Temperature, Humidity
from . import db
from .utility.apiutility import getWeatherData

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    weatherData = getWeatherData(db, Temperature, Humidity)
    return render_template("weather.html", weather=weatherData)
    
@views.route("/api/weather",  methods=['GET'])
def updateWeather():
    weatherData = getWeatherData(db, Temperature, Humidity)
    return jsonify(weatherData)
