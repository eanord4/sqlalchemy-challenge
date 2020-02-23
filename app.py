# Eric Nordstrom
# Homework #10 for UT Data boot camp
# Flask app using SQLAlechemy with SQLite database


## setup ##

# dependencies
from flask import Flask
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# initializations
app = Flask(__name__)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
assert Base.classes.keys() == ["measurement", "station"]
session = Session(engine)

# ORM classes
Measurement = Base.classes.measurement
Station = Base.classes.station


## app routes and functionality ##


@app.route("/")
def home():
    return


@app.route("/api/v1.0/precipitation")
def precip():
    return


@app.route("/api/v1.0/stations")
def stations():
    return


@app.route("/api/v1.0/tobs")
def tobs():
    return


@app.route("/api/v1.0/<path:dates>")
def temps_from_range(dates):
    """accepts a single start date or both a start and an end date (slash-delimited)"""

    # validate dates
    dates = dates.split("/")
    if len(dates) > 2:
        raise ValueError("Number of dates must be (1) or (2).")

    # get dates
    start = dates[0]
    end = (
        dates[1]
        if len(dates) == 2
        else session.query(func.max(Measurement.date)).all()[0][0]
    )

    return pd.DataFrame(

        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        )
        .filter(Measurement.date >= start)
        .filter(Measurement.date <= end)
        .all(),

        columns=["min", "avg", "max"],
        index = [f"temperatures from {start} to {end}:"]

    )


## run app ##
if __name__ == "__main__":
    app.run(debug=True)
