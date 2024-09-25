'''
Class to deal with obtaining data from Amadeus
Flight website.
'''


class FlightData:

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops) -> None:
        self.price = price
        self.origin_airport = origin_airport
        self.destinatin_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops

    def get_cheapest_flights(data):
        '''
        Get the cheapest flights
        Should return N/A if no data found
        '''

        # H andle missing data

        if data is None or not data['data']:
            print('No flight data')
            return FlightData(
                price='N/A',
                origin_airport='N/A',
                destination_airport='N/A',
                out_date='N/A',
                return_date='N/A',
                stops='N/A')

        # First flight in JSON:

        first_flight = data['data'][0]
        lowest_price = float(first_flight['price']['grandTotal'])
        nr_stops = len(first_flight['itineraries'][0]['segments']) - 1
        origin = first_flight['itineraries'][0]['segments'][0][
            'departure']['iataCode']
        destination = first_flight['itineraries'][0]['segments'][0]['departure']['iataCode']
        out_date = first_flight['itineraries'][0]['segments'][0]['departure']['at'].split('T')[
            0]
        return_date = first_flight['itineraries'][1]['segments'][0]['departure']['at'].split('T')[
            0]

        # initialise FlightData with the first cheapest flight
        cheapest_flight = FlightData(
            lowest_price, origin, destination, out_date, return_date, nr_stops)

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
                cheapest_flight = FlightData(
                    lowest_price, origin, destination, out_date, return_date, nr_stops)
                print(f'Lowest price to {destination} is £{[lowest_price]}')
        return cheapest_flight
