# Import Dependencies

import board
import pandas as pd
from busio import I2C
import adafruit_bme680
from datetime import datetime, timedelta
import time
import requests
import mysql.connector
import json
import sqlalchemy

# read database config file
with open("config.json") as config:
    param = json.load(config)

# Create library object using Bus I2C port
i2c = I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

# Read data from sensors
while True:
    # Create the now variable to capture the current moment
    TimeStamp = datetime.now()
    Temperature = round((bme680.temperature * 9/5) + 32, 2)
    Gas = round(bme680.gas, 2)
    Humidity = round(bme680.humidity, 2)
    Pressure = round(bme680.pressure, 2)
    Altitude = round(bme680.altitude, 2)

    now = datetime.strftime(TimeStamp,"%Y-%m-%dT%H:%M:%S")
    # Adding collected measurements into dataframe
    data = pd.DataFrame([
        {
            "TimeStamp": now,
            "Temperature": Temperature,
            "Gas": Gas,
            "Humidity": Humidity,
            "Pressure": Pressure,
            "Altitude": Altitude
        }
    ])

    # Try establishing connection with database
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
                data.to_sql('sensordata', con = db_con, if_exists = 'append', index = False)
                db_con.close()
                # Dispose the engine
                engine.dispose()
            except OSError as e:
                print(e)
    except OSError as e:
        print(e)

    # Power BI API
    # BI Address to push the data to for Bi Services
    url = 'https://api.powerbi.com/beta/94cd2fa9-eb6a-490b-af36-53bf7f5ef485/datasets/4447c3ef-6e4c-4bcb-972b-a676d93a6240/rows?key=9CgiRxiuuPh9eA3BS2ndOm4hSYXS5t6JMBVgsQPc3Ng3UfPljIqv9Y5RnThCdwMdZg99jL5mMr7MitAT5dZlCA%3D%3D'
    # post/push data to the streaming API
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.request(
        method="POST",
        url=url,
        headers=headers,
        data=json.dumps(data.to_json())
    )
    data = pd.DataFrame()
    # Re-run the script at the beginning of every new minute.
    dt = datetime.now() + timedelta(minutes=1)
    dt = dt.replace(second=1)

    while datetime.now() < dt:
        time.sleep(1)

