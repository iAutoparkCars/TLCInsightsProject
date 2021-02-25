"""
AUTHOR
    Steven Bonilla
EXAMPLE
    python main.py
SYNOPSIS
    Follow the instruction prompts to enter optional Location and Dates
DESCRIPTION
    An interactive shell that uses TLC record trip data to give insights on trip fare and trip time estimates
    from borough to borough in NYC for green taxis, yellow taxis, and ridesharing (for-hire)
    When searching for specific time ranges, only data from Jan 2020 to July 2020 is available.

"""
import sys
import time
from prettytable import PrettyTable

# user defined objects
from model.query import SQLQuery
from utility.data_validator import LocationDateValidator
from utility.data_display import Format

def prompt_locations():
    """ Prompts user for location pair. If pair is valid, return valid pair as a list
    """
    while True:
        print('\nEnter BOROUGH start, end separated by a comma... or press ENTER to skip')
        print('\tEXAMPLE: Bronx, Manhattan')
        input_locations_raw = input("$ ")
        if len(input_locations_raw) == 0:
            return None
        elif input_locations_raw == "exit":
            sys.exit()

        locations_pair = input_locations_raw.upper().split(',')
        locations_pair = [locations_pair[0].strip(), locations_pair[1].strip()]
        is_valid_locations = LocationDateValidator.is_valid_location(locations_pair)

        if is_valid_locations:
            return locations_pair
        else:  # invalid location was entered
            print('\tInvalid borough(s) was entered. Only one pair allowed. Please check spelling is correct')


def prompt_dates():
    """ Prompts user for a pair of start and end dates. If pair is valid, return valid pair as a list
    """
    while True:
        print('\nEnter DATE start, end between Jan 1st and Jun 30th 2020 separated by a comma... '
              'or hit ENTER to skip')
        print('\tEXAMPLE: 2020-01-02, 2020-05-01  (format is YYYY-MM-DD)')
        input_dates_raw = input("$ ")
        if len(input_dates_raw) == 0:
            return None
        elif input_dates_raw == "exit":
            sys.exit()

        dates_pair = input_dates_raw.replace(" ", "").split(',')

        # datetime list pair
        valid_dates_pair = LocationDateValidator.get_valid_dates(dates_pair)

        if valid_dates_pair:
            return valid_dates_pair
        else:  # invalid location was entered
            print('\tInvalid date before January 2020 or after June 2020 entered. ')
            print('\tOnly range between 2020-01-01, 2020-06-30 is valid')


def run_program():
    location_pair = prompt_locations()
    timedate_pair = prompt_dates()
    time.sleep(0.2)
    print('\t\t ======================== FETCHING RESULTS... ======================== ')

    db_query = SQLQuery(location_pair, timedate_pair)
    types = ['Yellow Cab', 'Green Cab', 'Ridesharing']
    times = db_query.time_price_avgs[0]
    prices = db_query.time_price_avgs[1]

    table = PrettyTable()
    table.add_column('         ', ['average time', 'average price'])
    for i in range(len(times)):
        table.add_column(types[i], [Format.minutes(times[i]), Format.price(prices[i])])
    print(table)


def run_shell():
    print('=========================== WELCOME ==========================')
    print('================ Type \'exit\' any time to exit =================')
    while True:
        run_program()


def main():
    try:
        run_shell()
        sys.exit()
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
    except SystemExit as e:         # sys.exit()
        raise e
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))


if __name__ == '__main__':
    main()
