
#-----------------------------------------------------------------------------------------------------------------------
# Pushing data into Azure mysql
#-----------------------------------------------------------------------------------------------------------------------
# Importing Dependencies
import mysql.connector
import pandas as pd
import json
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table
from mysql.connector import Error

df = pd.read_csv('data/BackUp.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)

with open("paramteres/config.json") as config:
    param = json.load(config)

# Connecting to data warehouse
try:
    engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                      format(param['MyDemoServer'][0]['user'],
                                             param['MyDemoServer'][0]['password'],
                                             param['MyDemoServer'][0]['host'],
                                             param['MyDemoServer'][0]['database']), echo=False)

    # Cleaning the data from existing tables MetricValues and Metrics
    Epi_con = engine.connect()
    if Epi_con.connect():
        try:
            #Epi_con.execute("""TRUNCATE TABLE Sessions""")
            df.to_sql('sensordata', con=Epi_con, if_exists='append',chunksize=1000, index=False)
            Epi_con.close()
            engine.dispose()
        except OSError as e:
            print(e)
except OSError as e:
    print(e)