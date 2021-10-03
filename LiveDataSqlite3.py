# Import Dependencies
import sqlite3
import time
import board
from busio import I2C
import adafruit_bme680
import datetime
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
    now = datetime.datetime.now()
    
    TEMPERATURE = round(bme680.temperature,1)
    GAS = round(bme680.gas,1)
    HUMIDITY = round(bme680.humidity,1)
    PRESSURE = round(bme680.pressure,1)
    ALTITUDE = round(bme680.altitude,1)
    TIME_STAMP =(now)

    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute("INSERT INTO BME_DATA (TIME_STAMP, TEMPERATURE, GAS, HUMIDITY, PRESSURE, ALTITUDE) values(?,?,?,?,?,?)",(TIME_STAMP, TEMPERATURE, GAS, HUMIDITY, PRESSURE, ALTITUDE))
    conn.commit()
    # Test by printing data from table BME_DATA
    #for row in curs.execute("SELECT * FROM BME_DATA"):   
        #print (row)
    conn.close()
    print(TEMPERATURE, GAS, HUMIDITY, PRESSURE, ALTITUDE, TIME_STAMP)
    time.sleep(60)

