# Import dependencies
import mysql.connector
import json
import sqlalchemy

# read database config file
with open("parameters/config.json") as config:
    param = json.load(config)

# settting up the function with parameters
def dataupdate(TimeStamp,Temperature,Gas,Humidity, Pressure,Altitude):
    # Connecting to data warehouse
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
                sql = """INSERT INTO movies (TimeStamp,Temperature,Gas,Humidity, Pressure,Altitude)
                            VALUES (%s, %s, %s, %s,%s,%s) """
                # Establish the record with set of data to be taken form variables
                record = (TimeStamp,Temperature,Gas,Humidity, Pressure,Altitude)
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