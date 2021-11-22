import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)



Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    select = [Measurement.date,Measurement.prcp]
    queryresult = session.query(*select).all()
    session.close()

    precipitation = []
    for date, prcp in queryresult:
        Precipitation= {}
        Precipitation["Date"] = date
        Precipitation["Precipitation"] = prcp
        precipitation.append(prcp)

    return jsonify(precipitation)


@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    lateststr = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    date = dt.datetime.strptime(lateststr, '%Y-%m-%d')
    querydate = dt.date(date.year -1, date.month, date.day)
    data = [Measurement.date,Measurement.tobs]
    queryresult = session.query(*data).filter(Measurement.date >= querydate).all()
    session.close()
    

    tobsall = []
    for date, tobs in queryresult:
        dict = {}
        dict["Date"] = date
        dict["Tobs"] = tobs
        tobsall.append(dict)

    return jsonify(tobsall)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    data = [Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation]
    queryresult = session.query(*data).all()
    session.close()

    stations = []
    for station,name,lat,lon,el in queryresult:
        dict = {}
        dict["Station"] = station
        dict["Name"] = name
        dict["Lat"] = lat
        dict["Lon"] = lon
        dict["Elevation"] = el
        stations.append(dict)

    return jsonify(stations)



@app.route('/api/v1.0/start')
def start(start):
    session = Session(engine)
    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    tobs = []
    for min,avg,max in queryresult:
        dict = {}
        dict["Min"] = min
        dict["Average"] = avg
        dict["Max"] = max
        tobs.appendA(dict)

    return jsonify(tobs)

@app.route('/api/v1.0/start/stop')
def startstop(start,stop):
    session = Session(engine)
    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= stop).all()
    session.close()

    tobs = []
    for min,avg,max in queryresult:
        dict = {}
        dict["Min"] = min
        dict["Average"] = avg
        dict["Max"] = max
        tobs.append(dict)

    return jsonify(tobs)

if __name__ == '__main__':
    app.run(debug=True)