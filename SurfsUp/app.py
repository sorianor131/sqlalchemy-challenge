# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct
from flask import Flask, jsonify
import numpy as np


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Dates and temperature for the previous year: /api/v1.0/tobs<br/>"
        f"Min, Average & Max Temperatures for Start Date (yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Min, Average & Max Temperatures for Date Range (yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route("/api/v1.0/precipitation")
def precipitaion():
    session = Session(engine)

    """Return a list of all daily precipitation totals for the last year"""
    # Query daily precipitation
    start_date = '2016-08-23'
    sel = [measurement.date, 
        func.sum(measurement.prcp)]
    precipitation = session.query(*sel).\
            filter(measurement.date >= start_date).\
            group_by(measurement.date).\
            order_by(measurement.date).all()
   
    session.close()

    # Return a dictionary with date as key and precipitation as value
    prcp_dates = []
    prcp_totals = []

    for date, dailytotal in precipitation:
        prcp_dates.append(date)
        prcp_totals.append(dailytotal)
    
    precipitation_dict = dict(zip(prcp_dates, prcp_totals))

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():

    """Return a list of all weather stations"""
    sel = [measurement.station]
    stations = session.query(*sel).\
        group_by(measurement.station).all()

    # Convert list of tuples into normal list
    list_of_stations = list(np.ravel(stations)) 
    return jsonify(list_of_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    # Query the last 12 months of temperature observations for the most active station
    start_date = '2016-08-23'
    sel = [measurement.date, 
        measurement.tobs]
    temp = session.query(*sel).\
            filter(measurement.date >= start_date, measurement.station == 'USC00519281').\
            group_by(measurement.date).\
            order_by(measurement.date).all()

    dates = []
    temperature= []

    for date, observation in temp:
        dates.append(date)
        temperature.append(observation)
    
    tobs_dict = dict(zip(dates, temperature))

    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Calculate min, average and max temperature from start date
    # For testing purposes entered 2016-09-01....returned avg: 74.49, max: 87, min: 58
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()

    start_stats = []
    for min, avg, max in query_result:
        start_dict = {}
        start_dict["Min"] = min
        start_dict["Average"] = avg
        start_dict["Max"] = max
        start_stats.append(start_dict)

    return jsonify(start_stats)
  
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # For testing purposes entered 2016-08-23 - 2016-09-01....returned avg: 78.32, max: 84, min: 71
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()

    start_end_stats = []
    for min, avg, max in query_result:
        start_end_dict = {}
        start_end_dict["Min"] = min
        start_end_dict["Average"] = avg
        start_end_dict["Max"] = max
        start_end_stats.append(start_end_dict)
    
    return jsonify(start_end_stats)
  
if __name__ == '__main__':
    app.run(debug=True)

session.close()