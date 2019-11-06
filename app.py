import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify
from dateutil.parser import parse
import sqlalchemy
import datetime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func






engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()

Base = automap_base()

Base.prepare(engine, reflect=True)


Base.classes.keys()


Measurement = Base.classes.measurement
Station = Base.classes.station


session = Session(engine)

app = Flask(__name__)

df_selected_measurement = pd.read_sql("select date, prcp from Measurement where date between '2016-08-23' and '2017-08-23'", conn)
station_df = pd.read_sql("select * from Station", conn)
station_list = station_df['station'].to_json(orient='records')
df_selected_station = pd.read_sql("select date, tobs from Measurement where station = 'USC00519281' and date between '2016-08-23' and '2017-08-23'", conn)
selected_station_json = df_selected_station.to_json(orient='records')

@app.route('/')
def home():
    return (
        f"This is the Home Page :) <br/>"        
        f"The routes are listed below: <br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/(start_date)/(end_date)"
    )


@app.route('/api/v1.0/precipitation')
def precipitation():

    return jsonify(df_selected_measurement.to_dict(orient='records'))
   

@app.route('/api/v1.0/stations')
def stations():

    return station_list
    
@app.route('/api/v1.0/tobs')
def temp_monthly():


    return selected_station_json
    


if __name__ == '__main__':
    app.run()
