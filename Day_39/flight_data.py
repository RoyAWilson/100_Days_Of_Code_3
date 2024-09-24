'''
Class to deal with obtaining data from Amadeus
Flight website.
'''


class FlightData:

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date) -> None:
        self.price = price
        self.origin_airport = origin_airport
        self.destinatin_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date

    def get_cheapest_flights(data):
        '''
        Get the cheapest flights
        Should return N/A if no data found
        '''

        # H andle missing data

        if data is None or not data['data']:
            print('No flight data')
            return FlightData('N/A', 'N/A', 'N/A', 'N/A', 'N/A')

        # First flight in JSON:

        first_flight = data['data'][0]
        lowest_price = float(first_flight['price']['grandTotal'])
        origin = first_flight['itineraries'][0]['segments'][0][
            'departure']['iataCode']
        destination = first_flight['itineraries'][0]['segments'][0]['departure']['iataCode']
        out_date = first_flight['itineraries'][0]['segments'][0]['departure']['at'].split('T')[
            0]
        return_date = first_flight['itineraries'][1]['segments'][0]['departure']['at'].split('T')[
            0]

        # initialise FlightData with the first cheapest flight
        cheapest_flight = FlightData(
            lowest_price, origin, destination, out_date, return_date)

        for flight in data['data']:
            price = float(flight['price']['grandTotal'])
            if price < lowest_price:
                lowest_price = price
                origin = first_flight['itineraries'][0]['segments'][0][[
                    'departure']]['iataCode']
                destination = first_flight['itineraries'][0]['segments'][0]['departure']['iataCode']
                out_date = first_flight['itineraries'][0]['segments'][0]['departure']['at'].split('T')[
                    0]
                return_date = first_flight['itineraries'][1]['segments'][0]['departure']['at'].split('T')[
                    0]
                print(f'Lowest price to {destination} is £{[lowest_price]}')
        return cheapest_flight
