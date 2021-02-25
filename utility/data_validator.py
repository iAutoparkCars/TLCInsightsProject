import datetime

# static names of set that come from zone lookups csv data
BOROUGHS = {'EWR', 'MANHATTAN', 'BROOKLYN', 'STATEN ISLAND', 'BRONX', 'QUEENS'}
DATETIME_FORMAT = '%Y-%m-%d'

MIN_DATE = datetime.datetime.strptime('2020-01-01', DATETIME_FORMAT)
MAX_DATE = datetime.datetime.strptime('2020-07-01', DATETIME_FORMAT)


class LocationDateValidator:
    def __init__(self):
        pass

    # if two and only two locations are found in the set, then this is a valid pair
    @staticmethod
    def is_valid_location(pair):
        if not pair or len(pair) != 2:
            return False
        if pair[0] in BOROUGHS and pair[1] in BOROUGHS:
            return True
        else:
            return False

    @staticmethod
    def get_valid_dates(pair):
        """ return pair list for valid datetime pair, else return None"""
        if not pair or len(pair) != 2:
            return None
        try:
            date_start = datetime.datetime.strptime(pair[0], DATETIME_FORMAT)
            date_end = datetime.datetime.strptime(pair[1], DATETIME_FORMAT)

            if date_start >= MIN_DATE and date_end < MAX_DATE:
                return [date_start, date_end]
            else:
                return None
        except ValueError:
            print('\t\t Invalid format of date -- parsing error')
            return None
