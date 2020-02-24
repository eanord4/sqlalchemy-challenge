# Eric Nordstrom
# Homework #10 for UT Data boot camp
# Flask app using SQLAlechemy with SQLite database


## setup ##

# dependencies
from flask import Flask, jsonify, url_for
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

precip_route = "/api/v1.0/precipitation"
stations_route = "/api/v1.0/stations"
tobs_route = "/api/v1.0/tobs"
range_route = "/api/v1.0/<path:dates>"


@app.route("/")  # hopping around the pages seems to create a multi-threading error. couldn't figure out how to fix this.
def home():

    return (
        "<h1>Homework #10</h1>\n"
        "<h2>SQLAlchemy challenge</h2>\n"
        "<h2>Eric Nordstrom</h2>\n"
        "<h3>Endpoints</h3>\n"
        f"""<ol>
            <li><a href="{url_for('precip')}">{precip_route}</a></li>
            <li><a href="{url_for('stations')}">{stations_route}</a></li>
            <li><a href="{url_for('tobs')}">{tobs_route}</a></li>
            <li>
                /api/v1.0/start/end
                <ul><li>Insert start and optional end date with format 'yyyy-mm-dd'.</li></ul>
            </li>
        </ol>"""
    )


@app.route(precip_route)
def precip():

    today = session.query(func.max(Measurement.date)).all()[0][0]
    one_year_ago = str(int(today[:4]) - 1) + today[4:]

    return jsonify(
        dict(
            session.query(Measurement.date, Measurement.prcp).filter(
                Measurement.date > one_year_ago
            )
        )
    )


@app.route(stations_route)
def stations():
    return jsonify(dict(session.query(Station.id, Station.station)))


@app.route(tobs_route)
def tobs():

    today = session.query(func.max(Measurement.date)).all()[0][0]
    one_year_ago = str(int(today[:4]) - 1) + today[4:]

    return jsonify(
        dict(
            session.query(Measurement.date, Measurement.tobs).filter(
                Measurement.date > one_year_ago
            )
        )
    )


@app.route(range_route)
def temps_from_range(dates):
    """accepts a single start date or both a start and an end date (slash-delimited)"""

    # validate dates
    dates = dates.split("/")
    if dates[-1] == "":
        # allow for ending with a slash
        dates.pop()
    if len(dates) not in {1, 2}:
        raise ValueError(
            "Number of dates must be (1) or (2), separated by a '/'."
        )
    test_date = dates[0].split('-')
    if not(
        len(test_date) == 3
        and len(test_date[0]) == 4
        and len(test_date[1]) == 2
        and len(test_date[2]) == 2
        and ''.join(test_date).isnumeric()
    ):
        raise ValueError(
            "Use format 'yyyy-mm-dd' for date(s)."
        )

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
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .filter(Measurement.date <= end)
        .all(),
        columns=["min", "avg", "max"],
        index=["temp"],
    ).to_json()


## run app ##
if __name__ == "__main__":
    app.run(debug=True)
