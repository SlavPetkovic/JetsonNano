# Import Dependencies

import board
import pandas as pd
from busio import I2C
import adafruit_bme680
from datetime import datetime, timedelta
import time
import json


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
    print(data)