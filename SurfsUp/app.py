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
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    # session = Session(engine)
    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017, 8 ,23) - dt.timedelta(days=365)
    year_ago

    # Perform a query to retrieve the date and precipitation scores
    data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date > year_ago).\
        order_by(measurement.date).all()
        
    all_precipitation = []
    for date,precipitation in data:
            precipitation_dict = {}
            precipitation_dict[date] = precipitation
            
            all_precipitation.append(precipitation_dict)
    return jsonify(all_precipitation)

@app.route("/api/v1.0/station")
def station():
    stations = session.query(Station.station).all()
     # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # 
    year_ago = dt.date(2017, 8 ,23) - dt.timedelta(days=365)
    year_ago
    yearly = session.query(measurement.tobs).filter(measurement.date > year_ago).\
    filter(measurement.station == 'USC00519281').all()
    
     # Convert list of tuples into normal list
    all_tobs = list(np.ravel(yearly))

    return jsonify(all_tobs)

if __name__ == '__main__':
    app.run(debug=True)
