'''
Find cheap flights and email alert.
'''

import os
import requests
from datetime import datetime, timedelta
import time
import smtplib
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from dotenv import load_dotenv

load_dotenv()

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()

ORIGIN_CITY_DATA = 'LON'

# Update airport codes in the google sheet:

# for row in sheet_data:
#     if row['iataCode'] == '':
#         row['iataCode'] = flight_search.get_destination_code(row['city'])
#         time.sleep(2)
# data_manager.destination_data = sheet_data
# data_manager.update_destination_codes()

# Initiate flight search

tomorrow = datetime.now().date() + timedelta(days=1)
six_months_from_today = datetime.now().date() + timedelta(days=(6 * 30))
flights_string = ''
for destination in sheet_data:
    print(f'getting flights for {destination['city']}....')
    flights = flight_search.check_flights(
        ORIGIN_CITY_DATA,
        destination['iataCode'],
        from_time=tomorrow,
        to_time=six_months_from_today
    )
    cheapest_flight = FlightData.get_cheapest_flights(data=flights)
    print(f'Destination City {destination['city']}: Cheapest flight {
          cheapest_flight.price}')
    time.sleep(2)
    flight_string = flights_string + f'Destination City {destination['city']}: Cheapest flight {
        cheapest_flight.price}\n'

# Email results to self:

G_MAIL = os.getenv('G_MAIL')
G_PASS = os.getenv('G_PASS')
H_MAIL = os.getenv('AMA_USER')
print(flight_string)
with smtplib.SMTP(host='smtp.gmail.com') as connection:
    connection.starttls()
    connection.login(user=G_MAIL, password='G_PASS')
    connection.sendmail(from_addr='G_MAIL', to_addrs=H_MAIL,
                        msg=f'subhect:Cheap Flights\n\n{flight_string}')
