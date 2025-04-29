import pyodbc
import time
def get_db_connection():
    while True:
       try:
          conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
             'SERVER=192.168.1.168;'
               'DATABASE=CRUD_DB;'
                'UID=sa;'
               'PWD=Sql@2019'
          )
          print("Database connection was successful")
          return conn
       except Exception as error:
            print("Failed")
            print("Error", error)
            time.sleep(2)