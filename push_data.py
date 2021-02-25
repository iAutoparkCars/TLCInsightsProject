"""
AUTHOR
    Steven Bonilla
EXAMPLE
    python push_data.py
SYNOPSIS
    Populates Azure SQL DB
DESCRIPTION
    A script that populates an Azure SQL DB with TLC data found in the /data directory of this project
    The bulk data is partitioned into manageable sized chunks at which a SAMPLE_SIZE is taken from each chunk
    and inserted for later querying.
    There are three main tables in the DB: Yellow Cab, Green Cab, and HVFHV (Ridesharing)
    Uncomment appropriate lines below to populate appropriate table
"""

import pyodbc
import datetime
import pandas as pd

MONTH_END = 6
CHUNKSIZE = 10 ** 6
SAMPLE_SIZE_PER_CHUNK = 25
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def parse_csv_rideshare(month):
    filename = 'data/fhvhv_tripdata_2020-0'+str(month)+'.csv'
    chunk_count = 1
    full_list = []
    for chunk in pd.read_csv(filename, chunksize=CHUNKSIZE, usecols=['pickup_datetime', 'dropoff_datetime',
                                                  'PULocationID', 'DOLocationID']):
        print(chunk_count, len(chunk), chunk.index)
        chunk_list = process_chunk_rideshare(chunk)
        full_list.extend(chunk_list)
        chunk_count += 1

    write_to_db('dbo.rideshare_tripdata', full_list, False)


def process_chunk_rideshare(df):
    size = len(df)
    multiple = int(size / SAMPLE_SIZE_PER_CHUNK)  # take a sample incrementally from a chunk
    start = int(df.index.start)
    end = int(df.index.stop)

    row_list = []
    i = 0
    while i < size:
        if start + i > end:  # out of bounds for this chunk
            break
        trip_time_minutes = calculate_timestamp_difference(df.loc[start + i, "pickup_datetime"],
                                                           df.loc[start + i, "dropoff_datetime"],
                                                           DATE_TIME_FORMAT)
        pu_location_id = int(df.loc[start + i, "PULocationID"])
        do_location_id = int(df.loc[start + i, "DOLocationID"])

        # convert tuple to list, add to final rowList
        row_list.append(list((df.loc[start + i, "pickup_datetime"],
                              df.loc[start + i, "dropoff_datetime"],
                              pu_location_id,
                              do_location_id,
                              trip_time_minutes,
                              idBoroughMap[pu_location_id],
                              idBoroughMap[do_location_id])))
        i += multiple
    return row_list


def parse_csv_green(month):
    filename = 'data/green_tripdata_2020-0'+str(month)+'.csv'
    chunk_count = 1
    full_list = []
    for chunk in pd.read_csv(filename, chunksize=CHUNKSIZE, usecols=['lpep_pickup_datetime', 'lpep_dropoff_datetime',
                                                  'PULocationID', 'DOLocationID', 'total_amount']):
        print(chunk_count, len(chunk), chunk.index)
        chunk_list = process_chunk_green(chunk)
        full_list.extend(chunk_list)
        chunk_count += 1
    write_to_db('dbo.green_tripdata', full_list, True)


def process_chunk_green(df):
    size = len(df)
    multiple = int(size / SAMPLE_SIZE_PER_CHUNK)  # take a sample incrementally from a chunk
    start = int(df.index.start)
    end = int(df.index.stop)

    row_list = []
    i = 0
    while i < size:
        if start + i > end:  # out of bounds for this chunk
            break
        trip_time_minutes = calculate_timestamp_difference(df.loc[start + i, "lpep_pickup_datetime"],
                                                           df.loc[start + i, "lpep_dropoff_datetime"],
                                                           DATE_TIME_FORMAT)
        pu_location_id = int(df.loc[start + i, "PULocationID"])
        do_location_id = int(df.loc[start + i, "DOLocationID"])

        # convert tuple to list, add to final rowList
        row_list.append(list((df.loc[start + i, "lpep_pickup_datetime"],
                              df.loc[start + i, "lpep_dropoff_datetime"],
                              pu_location_id,
                              do_location_id,
                              df.loc[start + i, "total_amount"],
                              trip_time_minutes,
                              idBoroughMap[pu_location_id],
                              idBoroughMap[do_location_id])))
        i += multiple
    return row_list


def parse_csv_yellow(month):
    filename = 'data/yellow_tripdata_2020-0'+str(month)+'.csv'
    chunk_count = 1
    full_list = []    # will use this list to insert values
    for chunk in pd.read_csv(filename, chunksize=CHUNKSIZE, usecols=['tpep_pickup_datetime', 'tpep_dropoff_datetime',
                                                  'PULocationID', 'DOLocationID', 'total_amount']):
        print(chunk_count, len(chunk), chunk.index)
        chunk_list = process_chunk_yellow(chunk)
        full_list.extend(chunk_list)
        chunk_count += 1

    write_to_db('dbo.yellow_tripdata', full_list, True)


def process_chunk_yellow(df):
    size = len(df)
    multiple = int(size / SAMPLE_SIZE_PER_CHUNK)   # take a sample incrementally from a chunk
    start = int(df.index.start)
    end = int(df.index.stop)

    row_list = []
    i = 0
    while i < size:
        if start + i > end:    # out of bounds for this chunk
            break
        trip_time_minutes = calculate_timestamp_difference(df.loc[start + i, "tpep_pickup_datetime"],
                                                           df.loc[start + i, "tpep_dropoff_datetime"],
                                                           DATE_TIME_FORMAT)
        pu_location_id = int(df.loc[start + i, "PULocationID"])
        do_location_id = int(df.loc[start + i, "DOLocationID"])

        # convert tuple to list, add to final rowList
        row_list.append(list((df.loc[start + i, "tpep_pickup_datetime"],
                              df.loc[start + i, "tpep_dropoff_datetime"],
                              pu_location_id,
                              do_location_id,
                              df.loc[start + i, "total_amount"],
                              trip_time_minutes,
                              idBoroughMap[pu_location_id],
                              idBoroughMap[do_location_id])))
        i += multiple
    return row_list


def calculate_timestamp_difference(pu_timestamp, do_timestamp, time_format):
    pu_datetime = datetime.datetime.strptime(pu_timestamp, time_format)
    do_datetime = datetime.datetime.strptime(do_timestamp, time_format)
    return round((do_datetime - pu_datetime).total_seconds() / 60.0)


def prepare_insert_statement(table_name, has_ride_amount):
    if has_ride_amount:
        return f"INSERT INTO {table_name} " \
                       f"(pickup_datetime,dropoff_datetime, " \
                       f"PULocationID, DOLocationID, " \
                       f"total_amount, trip_time, " \
                       f"PUBorough, DOBorough) " \
                       f"VALUES (?,?,?,?,?,?,?,?)"
    else:
        return f"INSERT INTO {table_name} " \
               f"(pickup_datetime,dropoff_datetime, " \
               f"PULocationID, DOLocationID, " \
               f"trip_time, " \
               f"PUBorough, DOBorough) " \
               f"VALUES (?,?,?,?,?,?,?)"


def write_to_db(table_name, values_list, has_ride_amount):
    insert_statement = prepare_insert_statement(table_name, has_ride_amount)

    server = 'tcp:nyctripdata.database.windows.net'
    database = 'TripDB'
    username = 'iAutoparkCars'
    password = 'Microsoftnyc0'
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = conn.cursor()
    cursor.executemany(insert_statement, values_list)
    cursor.commit()
    cursor.close()
    print(f'{len(values_list)} rows inserted into {table_name}')


def load_location_ids():
    filename = 'data/zone_lookup.csv'
    id_to_borough = {}  # map of locationId -> Borough name (string)
    for df in pd.read_csv(filename, chunksize=CHUNKSIZE, usecols=['LocationID', 'Borough']):
        for index, row in df.iterrows():
            id_to_borough[row['LocationID']] = row['Borough']
    return id_to_borough


current_month = 1
idBoroughMap = load_location_ids()
while current_month <= MONTH_END:
    print(f'\t Starting new month {current_month}')
    """ UNCOMMENT lines below to populate green, yellow, or rideshare/for-hire database """
    # parse_csv_rideshare(current_month)
    # parse_csv_yellow(current_month)
    # parse_csv_green(current_month)
    current_month += 1
