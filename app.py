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


 # Calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date
@app.route("/api/v1.0/<start>")
def single_date(start):
    session = Session(engine)
    Start_Date = dt.datetime.strptime(start,"%Y-%m-%d")

    result_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
    filter(Measurement.date >= Start_Date).all()
	# Close the Query
    session.close() 
	
    result = list(np.ravel(result_stats))

	# Jsonify summary
    return jsonify(result)



#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start

@app.route("/api/v1.0/<start>/<end>")
def trip_dates(start,end):
    session = Session(engine)
	Start_Date = dt.datetime.strptime(start,"%Y-%m-%d")
	End_Date = dt.datetime.strptime(end,"%Y-%m-%d")

	result_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
	filter(Measurement.date.between(Start_Date,End_Date)).all()
	# Close the Query
	session.close()    
	
	result = list(np.ravel(result_stats))

	# Jsonify summary
	return jsonify(result)




if __name__ == '__main__':
    app.run(debug=True)