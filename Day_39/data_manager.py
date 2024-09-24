'''
Manage data for api calls
'''

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv, dotenv_values

# Load environment variables from .env files:

SHEETY_PRICES_ENDPOINT = r'https://api.sheety.co/910a5fdd3891a4d6b2187a612cce0326/flights/sheet1'
load_dotenv()


class DataManager:
    '''
    Set up data management
    '''

    def __init__(self) -> None:
        '''
        Initialise varilables
        '''
        self._user = os.getenv('SHEETY_USER_NAME')
        self._password = os.getenv('SHEETY_PASSWORD')
        # self._authorization = HTTPBasicAuth(self._user, self._password)
        self.aut = {self._user: self._password}
        self.destination_data = {}

    def get_destination_data(self) -> dict:
        '''
        Read data from Sheety
        '''

        response = requests.get(
            url=SHEETY_PRICES_ENDPOINT, headers=self.aut)
        data = response.json()
        self.destination_data = data['sheet1']
        return self.destination_data

    # Update the IATA Codes in the google sheet using put command:

    def update_destination_codes(self):
        '''
        Update destination codes in the google sheet.
        '''
        for city in self.destination_data:
            new_data = {
                'sheet1': {
                    'iataCode': city['iataCode'],

                }
            }
            response = requests.put(
                url=f'{SHEETY_PRICES_ENDPOINT}/{city[id]}',
                json=new_data, headers=self.aut
            )

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                'sheet1': {
                    'iataCode': city['iataCode']
                }
            }
            response = requests.put(
                url=f'{SHEETY_PRICES_ENDPOINT}/{city["id"]}',
                json=new_data,
                headers=self.aut,
            )
        # print(response.text)
