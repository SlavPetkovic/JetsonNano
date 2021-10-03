# Import Dependencies
import sqlite3
import time
import board
from busio import I2C
import adafruit_bme680
from datetime import datetime
import requests

import mysql.connector
import json
import sqlalchemy

# read database config file
with open("config.json") as config:
    param = json.load(config)

# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25


# Using while loop capture the data in variables and store it in database
while True:
    # Create the now variable to capture the current moment
    TimeStamp = datetime.now()
    Temperature = round((bme680.temperature * 9/5) + 32, 2)
    Gas = round(bme680.gas, 2)
    Humidity = round(bme680.humidity, 2)
    Pressure = round(bme680.pressure, 2)
    Altitude = round(bme680.altitude, 2)

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
                sql = """INSERT INTO sensordata (TimeStamp, Temperature, Gas, Humidity, Pressure, Altitude)
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

# API Post

    url = 'https://api.powerbi.com/beta/94cd2fa9-eb6a-490b-af36-53bf7f5ef485/datasets/2a7a2529-dbfd-4c32-9513-7d5857b61137/rows?key=nS3bP1Mo4qN9%2Fp6XJcTBgHBUV%2FcOZb0edYrK%2BtVWDg6iWwzRtY16HWUGSqB9YsqF3GHMNO2fe3r5ltB7NhVIvw%3D%3D'

    now = datetime.strftime(
        datetime.now(),
        "%Y-%m-%dT%H:%M:%S"
    )

    data = [
        {
            "TimeStamp": now,
            "Temperature": Temperature,
            "Gas": Gas,
            "Humidity": Humidity,
            "Pressure": Pressure,
            "Altitude": Altitude
        }
    ]

    # post/push data to the streaming API
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.request(
        method="POST",
        url=url,
        headers=headers,
        data=json.dumps(data)
    )

    time.sleep(60)
