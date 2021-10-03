# Import Dependencies
import sqlite3
import time
import board
from busio import I2C
import adafruit_bme680
import datetime
import mysql.connector
import json
import sqlalchemy

# read database config file
with open("parameters/config.json") as config:
    param = json.load(config)

# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

# Define database name to which data will be stored
dbname = 'Prometheus.db'


# Using while loop capture the data in variables and store it in database
while True:
    # Create the now variable to capture the current moment
    TimeStamp = datetime.datetime.now()
    Temperature = round(bme680.temperature,1)
    Gas = round(bme680.gas,1)
    Humidity = round(bme680.humidity,2)
    Pressure = round(bme680.pressure,2)
    Altitude = round(bme680.altitude,2)

    try:
        engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                          format(param['MyDemoServer'][0]['user'],
                                                 param['MyDemoServer'][0]['password'],
                                                 param['MyDemoServer'][0]['host'],
                                                 param['MyDemoServer'][0]['database']), echo=False)

        # Cleaning the data from existing tables MetricValues and Metrics
        db_con = engine.connect()
        if db_con.connect():
            try:
                sql = """INSERT INTO movies (TimeStamp, Temperature, Gas, Humidity, Pressure, Altitude)
                            VALUES (%s, %s, %s, %s, %s, %s) """
                # Establish the record with set of data to be taken form variables
                record = (TimeStamp, Temperature, Gas, Humidity, Pressure, Altitude)
                # Execute sql with collected records
                db_con.execute(sql, record)
                # Close connection
                db_con.close()
                # Dispose the engine
                engine.dispose()
            except OSError as e:
                print(e)
    except OSError as e:
        print(e)

    time.sleep(1)

