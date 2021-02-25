import pyodbc
import datetime

first = 'steve'
shouldAdd = False
DATETIME_FORMAT = '%Y-%m-%d'
MIN_DATE = datetime.datetime.strptime('2020-01-01', DATETIME_FORMAT)
MAX_DATE = datetime.datetime.strptime('2020-03-01', DATETIME_FORMAT)

server = 'tcp:nyctripdata.database.windows.net'
database = 'TripDB'
username = 'iAutoparkCars'
password = 'Microsoftnyc0'
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = conn.cursor()

table_name = 'dbo.yellow_tripdata'
date_pair = MIN_DATE, MAX_DATE

query = f"SELECT AVG(trip_time) as avg_trip_time FROM {table_name} "
#query = query + f"WHERE UPPER(PUBorough) = \'{location_pair[0]}\' AND " \
#                    f"UPPER(DOBorough) = \'{location_pair[1]}\' "
if date_pair:
    query = query + f" WHERE pickup_datetime >= \'{date_pair[0]}\' AND " \
                       f"dropoff_datetime < \'{date_pair[1]}\' "

cursor.execute(query)
res = cursor.fetchone()
print(res[0])