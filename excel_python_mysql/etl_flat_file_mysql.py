import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
import pymysql
import configparser

# read data from source
df = pd.read_csv('/mnt/c/Users/Jagua/Desktop/Us_Statstique_Crime/Crime_Data_from_2020_to_Present_20240516.csv')

# Read the configuration file

config = configparser.ConfigParser()
config.read('mysql_credentials.ini')

# Access the data
database_host = config.get('connection', 'host')
database_port = config.getint('connection', 'port')
database_user = config.get('connection', 'user')
database_password = config.get('connection', 'password')

connection_string = f"mysql+pymysql://{database_user}:{database_password}@{database_host}"
engine = create_engine(connection_string)

def create_database_if_not_exists(connection_string, db_name):
    engine = create_engine(connection_string)
    with engine.connect() as conn:
        result = conn.execute(text(f"SHOW DATABASES LIKE '{db_name}'"))
        if result.fetchone() is None:
            conn.execute(text(f"CREATE DATABASE {db_name}"))
            print(f"Database '{db_name}' created successfully.")
        else:
            print(f"Database '{db_name}' already exists.")

create_database_if_not_exists(connection_string, 'los_angeles_crime')


# load data to mysql

def load(df, tbl, connection_string):
    try:
        rows_imported = 0
        engine = create_engine(connection_string)
        print(f'importing rows {rows_imported} to {rows_imported + len(df)}...')
        # save df to mysql
        df.to_sql(f"la_crime_{tbl}", engine, if_exists='replace', index=False)
        rows_imported += len(df)

        print("Data imported successfully.")
    except Exception as e:
        print("Data load error: " + str(e))
    
# execute
connection_string = f"mysql+pymysql://{database_user}:{database_password}@{database_host}/{'los_angeles_crime'}"
load(df, 'los_angeles_crime_data', connection_string)
