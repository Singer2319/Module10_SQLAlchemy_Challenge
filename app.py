# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
#Passenger = Base.classes.passenger
Station = Base.classes.station
Measurement = Base.classes.measurement


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    #list available api routes
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


#Return query results from your precipitation analysis
@app.route("/api/v1.0/precipitation")
def percipitation():
    #query
    a_session = Session(engine)
    oneyrpast = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    results = a_session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= oneyrpast).all()
    a_session.close()

    #convert query results to a dictionary
    precipitation_results = []
    for i in results:
        (date, temp) = i
        precipitation_results.append({"date" : date, "temp" : temp})

    return(jsonify(precipitation_results))


#Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    #query
    a_session = Session(engine)
    results = a_session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    a_session.close()
    
    #convert query results to a dictionary
    station_results = []
    for i in results:
        (id, station, name, lat, lon, elev) = i
        station_results.append({"id" : id, "station" : station, "name" : name, "latitude" : lat, "longitude" : lon, "elevation" : elev})

    return(jsonify(station_results))


@app.route("/api/v1.0/tobs")
def temperatures():
    #query
    a_session = Session(engine)
    results = a_session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()
    a_session.close()

    #convert query results to a dictionary
    temp_results = []
    for i in results:
        (station, date, temp) = i
        temp_results.append({"station" : station, "date" : date, "temperature" : temp})

    return(jsonify(temp_results))


@app.route("/api/v1.0/<start>")
def start_temp(start_date):
    #query
    a_session = Session(engine)
    results = a_session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    a_session.close()

    #convert query results to a dictionary
    start_temp = []
    for i in results:
        (min, avg, max) = i
        start_temp.append({"Min Temp" : min, "Avg Temp" : avg, "Max Temp" : max})


    return jsonify(start_temp)

@app.route("/api/v1.0/<start>/<end>")
def start_end_temps(start, end): 
    a_session = Session(engine)

    results = a_session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    a_session.close()

     # Create a dictionary and append to the temps list
    temps = []

    for i in results:
        (min, avg, max) = i
        temps.append({"Min Temp" : min, "Avg Temp" : avg, "Max Temp" : max})

    return jsonify(temps)



if __name__ == '__main__':
    app.run(debug=True)