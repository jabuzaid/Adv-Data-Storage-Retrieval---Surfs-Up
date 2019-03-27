# General imports:
import pandas as pd
import numpy as np
import datetime as dt
from flask import Flask, jsonify

# sqlalchemy imports:
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# We are creating a flask app!
app = Flask(__name__)

# connect to the database
engine = create_engine('sqlite:///hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine) # allows us to session.query

# We are telling flask what to return when a client hits '/'
@app.route('/')
def welcome():
    return(
        f"Welcome to the Hawaii Climate Analysis<br/>"
        f"Available Routes</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end></br>")

@app.route('/api/v1.0/precipitation')
def precipitation_func():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > prev_year).all()

    precip = {date: prcp for date, prcp in precipitation}

    return jsonify(precip)

if __name__ == '__main__':
    app.run(debug=True) # this line starts a server