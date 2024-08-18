
# Crime Data Import and Database Setup

This script demonstrates how to import crime data from a CSV file into a MySQL database using Python. It involves reading data from a CSV file, creating a database if it doesn't exist, and loading the data into a MySQL table.

<img src="https://github.com/Sendo-A/etl_workflow_python_analysis/blob/main/excel_python_mysql/Importing%20proof.PNG" alt="workflow" width="800">

## Prerequisites

- Python 3.x
- Required Python packages:
  - `pandas`
  - `numpy`
  - `sqlalchemy`
  - `pymysql`
  - `configparser`

## Installation

Install the required packages using pip:

```bash
pip install pandas numpy sqlalchemy pymysql configparser
```

## Configuration

Create a configuration file named `mysql_credentials.ini` with the following structure:

```ini
[connection]
host = your_host
port = your_port
user = your_username
password = your_password
```

Replace `your_host`, `your_port`, `your_username`, and `your_password` with your MySQL database credentials.

## Script Overview

1. **Read Data from CSV File**

   The script reads a CSV file containing crime data.

   ```python
   df = pd.read_csv('/path/to/Crime_Data_from_2020_to_Present_20240516.csv')
   ```

2. **Read Configuration**

   The script reads MySQL database credentials from the `mysql_credentials.ini` file.

   ```python
   config = configparser.ConfigParser()
   config.read('mysql_credentials.ini')
   ```

3. **Create Database**

   The script defines a function to create a database if it does not already exist.

   ```python
   def create_database_if_not_exists(connection_string, db_name):
       engine = create_engine(connection_string)
       with engine.connect() as conn:
           result = conn.execute(text(f"SHOW DATABASES LIKE '{db_name}'"))
           if result.fetchone() is None:
               conn.execute(text(f"CREATE DATABASE {db_name}"))
               print(f"Database '{db_name}' created successfully.")
           else:
               print(f"Database '{db_name}' already exists.")
   ```

   The database `los_angeles_crime` is created if it does not exist.

4. **Load Data to MySQL**

   The script defines a function to load data from a DataFrame into a MySQL table.

   ```python
   def load(df, tbl, connection_string):
       try:
           rows_imported = 0
           engine = create_engine(connection_string)
           print(f'importing rows {rows_imported} to {rows_imported + len(df)}...')
           df.to_sql(f"la_crime_{tbl}", engine, if_exists='replace', index=False)
           rows_imported += len(df)
           print("Data imported successfully.")
       except Exception as e:
           print("Data load error: " + str(e))
   ```

   The data is loaded into the table `la_crime_los_angeles_crime_data` in the `los_angeles_crime` database.

5. **Execution**

   The script executes the functions to create the database and load the data.

   ```python
   connection_string = f"mysql+pymysql://{database_user}:{database_password}@{database_host}/{'los_angeles_crime'}"
   load(df, 'los_angeles_crime_data', connection_string)
   ```

## Notes

- Update the path to the CSV file and ensure it is correctly referenced in the script.
- Ensure MySQL server is running and accessible with the provided credentials.
- The `configparser` library is used for reading configuration settings, which makes it easier to manage credentials securely.

