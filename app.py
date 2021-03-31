#creatinf dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Setting up the Database
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def Home():
    """List all routes that are available."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

    # Convert the query results to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement).all()
    session.close()
    
    # Create a dictionary
    precipitation_results = []
    for each_row in results:
        dt_dict = {}
        dt_dict["date"] = each_row.date
        dt_dict["tobs"] = each_row.tobs
        precipitation_results.append(dt_dict)

    return jsonify(precipitation_results)

#Return a JSON list of stations from the dataset
@app.route("/api/v1.0/station")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
	# Close the Query
    session.close()
	
    station_list = list(np.ravel(results))
    return jsonify(station_list)

# Query the dates and temperature observations of the most active station for the last year of data
@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    Last_Year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature_results = session.query(Measurement.tobs).filter(Measurement.date > Last_Year).all()
	# Close the Query
    session.close()

	# Convert list of tuples into normal list
    all_temperature = list(np.ravel(temperature_results))
    return jsonify(all_temperature)



if __name__ == '__main__':
    app.run(debug=True)