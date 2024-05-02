from sqlalchemy.sql import func
import decimal


#besides getWeatherData, the other functions are meant to be private.
#they could technically be used be elsewhere, but for the purposes of this application they are private

def _getDataForMeanCalc(db, dbTable):
    startIndex = db.session.query(func.count(dbTable.id)).scalar() - 5
    endIndex = db.session.query(func.count(dbTable.id)).scalar()
    #get the 5 most recent readings
    data = dbTable.query.order_by(dbTable.id).offset(startIndex).limit(endIndex - startIndex + 1).all()
    return data

def _getTemperatureData(db, Temperature):
    latestTempData = Temperature.query.order_by(Temperature.id.desc())
    meanTemp = None #decimal.decimal() normally

    #safe bet that if the first item found is None, then table is empty
    if latestTempData.first() is not None:
        temp = latestTempData.first().temperature
        tempDate = latestTempData.first().date

        def _getMeanTemperature(db, Temperature):
            meanTemp = decimal.Decimal()
            tempData = _getDataForMeanCalc(db, Temperature)
            for row in tempData:
                meanTemp += row.temperature                
            meanTemp /= len(tempData)
            return meanTemp
        
        if latestTempData.count() >= 5:
            meanTemp = _getMeanTemperature(db, Temperature)
    else:
        temp = None
        tempDate = None

    return temp, meanTemp, tempDate

def _getHumidityData(db, Humidity):
    latestHumidData = Humidity.query.order_by(Humidity.id.desc())
    meanHumid = None #decimal.decimal() normally
    
    if latestHumidData.first() is not None:
        humid = latestHumidData.first().humidity
        humidDate = latestHumidData.first().date

        def _getMeanHumidity(db, Humidity):
            meanHumid = decimal.Decimal()
            humidData = _getDataForMeanCalc(db, Humidity)
            for row in humidData:
                meanHumid += row.humidity 
            meanHumid /= len(humidData)
            return meanHumid

        if latestHumidData.count() >= 5:
            meanHumid = _getMeanHumidity(db, Humidity)
    else:
        humid = None
        humidDate = None
    return humid, meanHumid, humidDate

def getWeatherData(db, Temperature, Humidity):
    temp, meanTemp, tempDate = _getTemperatureData(db, Temperature)
    humid, meanHumid, humidDate = _getHumidityData(db, Humidity)

    weatherData = {
        'temperature': temp,
        'meanTemperature': meanTemp,
        'temperatureDate': tempDate,
        'humidity': humid,
        'meanHumidity': meanHumid,
        'humidityDate': humidDate,
    }
    return weatherData
