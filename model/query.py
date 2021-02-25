import pyodbc


class SQLQuery:
    time_price_avgs = ()

    def __init__(self, p1, p2):
        self.location_pair = p1
        self.date_pair = p2

        server = 'tcp:nyctripdata.database.windows.net'
        database = 'TripDB'
        username = 'iAutoparkCars'
        password = 'Microsoftnyc0'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                              'SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        self.cursor = conn.cursor()

        # execute queries and return values in the order of yellow, green, rideshare values
        SQLQuery.time_price_avgs = self.fetch_time_and_price_avgs(self.location_pair, self.date_pair)
        # print(self.time_price_avgs)
        self.cursor.close()

    # result is stored in a tuple of two lists (times list, prices list)
    def get_time_price_avgs(self):
        return SQLQuery.time_price_avgs

    def fetch_time_and_price_avgs(self, location_pair, date_pair):
        yellow_statement = self.prepare_avg_statement(location_pair, date_pair, 'dbo.yellow_tripdata')
        green_statement = self.prepare_avg_statement(location_pair, date_pair, 'dbo.green_tripdata')
        rideshare_statement = self.prepare_avg_statement(location_pair, date_pair, 'dbo.rideshare_tripdata')

        times = []
        prices = []

        # fetchone returns a tuple of time, price for yellow, green, rideshare (0 if not found)
        self.cursor.execute(yellow_statement)
        avg_yellow = self.cursor.fetchone()
        times.append(0 if not avg_yellow[0] else avg_yellow[0])
        prices.append(0 if not avg_yellow[1] else round(avg_yellow[1], 2))

        self.cursor.execute(green_statement)
        avg_green = self.cursor.fetchone()
        times.append(0 if not avg_green[0] else avg_green[0])
        prices.append(0 if not avg_green[1] else round(avg_green[1], 2))

        self.cursor.execute(rideshare_statement)
        avg_rideshare = self.cursor.fetchone()
        times.append(0 if not avg_rideshare[0] else avg_rideshare[0])
        prices.append(max(prices[0], prices[1]))

        # TIME list, PRICE list tuple
        return times, prices

    def prepare_avg_statement(self, location_pair, date_pair, table_name):
        # rideshare has no total_amount column, but yellow and green cabs do
        query = f"SELECT AVG(trip_time) as avg_trip_time FROM {table_name} " \
            if table_name == "dbo.rideshare_tripdata" \
            else f"SELECT AVG(trip_time) as avg_trip_time, AVG(total_amount) as avg_total FROM {table_name} "

        if location_pair or date_pair:
            query = query + f" WHERE  "
        if location_pair:
            query = query + f" UPPER(PUBorough) = \'{location_pair[0]}\' AND " \
                        f"UPPER(DOBorough) = \'{location_pair[1]}\'"
        if location_pair and date_pair:
            query = query + f" AND  "
        if date_pair:
            query = query + f" pickup_datetime >= \'{date_pair[0]}\' AND " \
                            f"dropoff_datetime < \'{date_pair[1]}\' "
        return query
