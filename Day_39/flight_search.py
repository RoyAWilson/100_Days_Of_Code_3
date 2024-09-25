'''
To search for flights using appi
'''

import os
from dotenv import load_dotenv, dotenv_values
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
import time
from data_manager import DataManager

IATA_ENDPOINT: str = 'https://test.api.amadeus.com/v1/reference-data/locations/cities'
FLIGHT_ENDPOINT: str = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
# TOKEN_ENDPOINT: str = 'https://test.api.amadeus.com/v1/security/oauth2/token/'
AUTH_ENDPOINT: str = "https://test.api.amadeus.com/v1/security/oauth2/token"

load_dotenv()


class FlightSearch:
    '''
    Search for flights.
    '''

    def __init__(self) -> None:
        '''
        Initialise vars and methods
        '''
        self._api_key: str = os.getenv('AMA_KEY')
        self._sec_key: str = os.getenv('AMA_SEC')
        self._user_name: str = os.getenv('AMA_USER')
        self._token: str = self._get_new_token()

        # self.get_destination = self.get_destination_code

    def _get_new_token(self) -> str:
        '''
        Obtain a bearer token from
        the Amadeus site.
        Return str : The token required for api access.
        '''

        # API end point = https://test.api.amadeus.com/v1/security/oauth2/token/
        # Values to send with post as key value pairs in tupples:
        # grant_type The value of client credentials
        # client_id The API key for the application
        # client_secret The API secret for the application
        # type 	The type of resource. The value will be amadeusOAuth2Token.
        # username 	Your username (email address).
        # application_name 	The name of your application.
        # client_id 	The API Key for your application
        # token_type 	The type of token issued by the authentication server. The value will be Bearer.
        # access_token 	The token to authenticate your requests.
        # expires_in 	The number of seconds until the token expires.
        # state 	The status of your request. Values can be approved or expired.
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "client_credentials",
                "client_id": os.getenv('AMA_KEY'),
                "client_secret": os.getenv('AMA_SEC')}
        response = requests.post(AUTH_ENDPOINT,
                                 headers=headers,
                                 data=data)
        access_token = response.json()['access_token']
        return access_token

    def get_destination_code(self, city_name: str) -> str:
        '''
        Get the city code from Amadeus
        Returns string, argument city_name'''

        HEADERS = {"Authorization": f"Bearer {self._token}"}
        QUERY = {
            'keyword': city_name,
            'max': '2',
            'include': 'AIRPORTS'
        }
        response = requests.get(
            url=IATA_ENDPOINT,
            headers=HEADERS,
            params=QUERY
        )

        print(f'Status Code = {
            response.status_code}.  AIRPORT IATA {response.text}')

        try:
            code = response.json()['data'][0]['iataCode']
        except IndexError:
            print(f'Key error, no code found for {city_name}')
            return ('N/A')
        except KeyError:
            print(f'KeyError, no code found for {city_name}')
            return ('Not Found')

        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):
        headers = {
            'Authorization': f'Bearer {self._token}'
        }
        query = {
            'originLocationCode': origin_city_code,
            'destinationLocationCode': destination_city_code,
            'departureDate': from_time.strftime('%Y-%m-%d'),
            'returnDate': to_time.strftime('%Y-%m-%d'),
            'adults': 1,
            'nonStop': 'true' if is_direct else 'false',
            'currencyCode': 'GBP',
            'max': '10'
        }
        response = requests.get(
            url=FLIGHT_ENDPOINT,
            headers=headers,
            params=query
        )
        if response.status_code != 200:
            print(f'Check flights response code: {response.status_code}')
            print('There was a problem with the flight search.\n'
                  'For details click the appi documentation\n'
                  'https: // developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api'
                  '-reference')
            print(f'Response body: {response.text}')
            return None
        return response.json()
