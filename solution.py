import argparse
import csv
import json
import itertools
from datetime import datetime, timedelta
from filters import Filters
from tests import Test

#Input handling:
parser = argparse.ArgumentParser(description="Flight combinations for a selected route between airports A -> B, \
                                                sorted by the final price for the trip")
parser.add_argument('csv_name', type=str, help="Name of csv file")
parser.add_argument('origin', type=str, help="Origin airport code")
parser.add_argument('destination', type=str, help="Destination airport code")
parser.add_argument('--bags', type=int, help="Number of requested bags", 
                    default=0, choices=range(10), required=False)
parser.add_argument('--return', action='store_true', help="Is it a return flight?", 
                    default=False, required=False)

#When --return argument, you can set delay before returning back
parser.add_argument('--days_away', type=int, help="", default=0, required=False)

#Set max landings between airports A -> B, default = 2, max_value = 5 (long time to calculate if >5)
parser.add_argument('--max_landings', type=int, help="Max number of landings on travel", 
                    default=None, required=False)
args = parser.parse_args()
conditions = vars(args)

#File handling with or without folder /example/
try:
    with open(args.csv_name, newline='') as csvfile:
        rows = csv.DictReader(csvfile, delimiter=',')
        flights = [dict(row) for row in rows]
except:
    with open(f'example/{args.csv_name}', newline='') as csvfile:
        rows = csv.DictReader(csvfile, delimiter=',')
        flights = [dict(row) for row in rows]
        
def save(json_data: json) -> None:
    """Saving data as json to file in main folder: data.json

    Args:
        json_data (json): Output data in json format
    """
    with open('data.json', 'w') as f:
        f.write(json_data)

class Search(Filters):
    """_summary_
    Search class for managing logic behind searching
    Args:
        Filters (class): inherited
    """
    def __init__(self, conditions: dict) -> None:
        super().__init__(conditions)
        self.city_pairs = set([(flight['origin'], flight['destination']) for flight in flights])
        self.middle_cities = {city for pair in self.city_pairs for city in pair 
                              if city != self.origin and city != self.destination}
        self.all_cities = {city for pair in self.city_pairs for city in pair}
        pass
    
    def plan_journey(self) -> list:
        """_summary_
        
        Calculate all journeys plane can fly as flight pairs. 
        There are all possibilities between origin and destination
        airports as list of pairs (tuples) between airports
        Permutations are calculated by input -> max landings (default = 2)
        For all journeys we set flight pairs to reach destination
        If input --return -> destination = origin
    
        Returns:
            list: Contains lists (journeys) with tuples (flight pairs) to destination
        """
        landings = self.max_landings
        if not landings:
            landings = len(self.middle_cities)
        flight_journeys = list()
        final_permutations_backward = list()
        final_permutations = list()
        
        #Permutations are caluclated from middle cities between origin and destination, 
        # 1 city is minimal number for travel with landing between
        for permutation_size in range(1, landings+1):
            if permutation_size > len(self.middle_cities):
                break
            permutations = [(self.origin, *perm, self.destination) for perm in 
                            itertools.permutations(self.middle_cities, permutation_size)]
            final_permutations.extend(permutations)
            if self.return_path:
                permutations_backward = [(self.destination, *perm, self.origin) for perm 
                                         in itertools.permutations(self.middle_cities, permutation_size)]
                final_permutations_backward.extend(permutations_backward)
        #With cycle done with all possible forward and backward combinations we will merge them \
            # together, if return trip was selected
        if self.return_path:
            #We add 1 pair flights to have all combinations possible
            final_permutations_backward.append((self.destination, self.origin))
            final_permutations.append((self.origin, self.destination))
            #Combine forward and backward trips to have all possibilities, \
            #than remove direct flights because we manage them in function no_landings_between_flights()
            final_yourneys = [permutation + permutation_backward for permutation in final_permutations 
                              for permutation_backward in final_permutations_backward 
                              if len(permutation + permutation_backward) > 4]
        else:
            final_yourneys = final_permutations
        for permutation in final_yourneys:
            flight_journeys.append([(origin, destination) for (origin, destination) 
                                    in zip(permutation, permutation[1:]) if origin != destination])
        
        return flight_journeys
    
    def flights_with_landings(self) -> list:
        """_summary_
        For all flight combinations between airports which are possible, apply filters and start searching
        Preparing data for searching flights with recursion
        
        Returns:
            list: Of dictionaries with possible flights to reach destination
        """
        # All possible permutation cities
        flight_journeys = self.plan_journey()
        self.filtered_routes = list()
        for flight_journey in flight_journeys:
            
            # All first possible flights from origin city, 
            #   filtered by number of bags - in cycle of yourneys from permutations
            first_flights = self.filter_direct_flights_by_cities(
                                self.filter_by_bags(flights), flight_journey[0][0], flight_journey[0][1])
            
            #For all first flights calculating youreys with flights to destination
            for first_flight in first_flights:
                self.yourney_flights = [None]*len(flight_journey) #initialisation of empty list for indexing flights
                self.compute_route(first_flight, flight_journey, 1)
        return self.filtered_routes
    
        
    def compute_route(self, flight: dict, flight_journey: list, idx: int) -> None:
        """Recursion method for calculating flight routes
        It takes first flight and combinations of all possible airport pairs 
        and compute all routes to destination which are possible

        Args:
            flight (dict): Flight which we want to tack time of another flight
            flight_journey (list of tuples): Computed pairs of airports to reach destination
            idx (int): index of flight in row
        """
        
        # If we reach destination and we want to return:
        # We manage time after back-flights will start calculating for Input: --return --days_away (default = 2)
        # All calculations are making for next flight 
        if flight_journey[idx][0] == self.destination:
            nextflights = self.filter_by_time(flight['arrival'], self.filter_direct_flights_by_cities(
                        self.filter_by_bags(flights), 
                        flight_journey[idx][0], flight_journey[idx][1]), True)
        else:
            nextflights = self.filter_by_time(flight['arrival'], self.filter_direct_flights_by_cities(
                        self.filter_by_bags(flights), 
                        flight_journey[idx][0], flight_journey[idx][1]))
        # Indexing this flight
        self.yourney_flights[idx-1] = flight
            
        # Calculating connections between next flights with recursion
        # If we reach destination (or origin if --return), saving result for later
        for nextflight in nextflights:
            if flight_journey[idx][1] == self.destination and not self.return_path:
                self.yourney_flights[idx] = nextflight
                if not self.yourney_flights in self.filtered_routes:
                    self.filtered_routes.append(self.yourney_flights)
                return
            if flight_journey[idx][1] == self.origin and self.return_path:
                self.yourney_flights[idx] = nextflight
                if not self.yourney_flights in self.filtered_routes:
                    self.filtered_routes.append(self.yourney_flights)
                return
            self.compute_route(nextflight, flight_journey, idx+1)

                 
    def no_landings_between_flights(self) -> list:
        """Calculating filtered flight routes only for direct flights

        Returns:
            list: All filtered flight routes from origin to destination, and backwards if --return argument
        """
        direct_trips = list()
        if conditions['return']:
            for flight in self.filter_direct_flights_by_cities(self.filter_by_bags(flights), 
                                                    self.origin, self.destination):
                for backflight in self.filter_by_time(flight['arrival'],
                        self.filter_direct_flights_by_cities(self.filter_by_bags(flights), 
                                                    self.destination, self.origin), True):
                    direct_trips.append([flight, backflight])
            filtered_routes = direct_trips
        else:
            filtered_routes = [[item] for item in self.filter_direct_flights_by_cities(
                            self.filter_by_bags(flights), self.origin, self.destination)]
        return filtered_routes
        
    def convert_to_json(self, list_of_trips: list) -> json:
        """Make JSON output from list of yourneys (with filtered flights: dict)

        Args:
            list_of_trips (list of dict): All flights from A -> B airports, or B -> A if --return argument

        Returns:
            JSON: Converted JSON with sorted routes by total_price
        """
        json_output = []
        #For every trip we are making expecting form as dictionary from assignment
        for trip in list_of_trips:
            json_object = {"flights": [flight for flight in trip], 
                        "bags_allowed": min([flight['bags_allowed'] for flight in trip]), 
                        "bags_count": self.number_of_bags, "destination": self.destination, "origin": self.origin, 
                        "total_price": sum([float(flight['base_price'])
                                        +(self.number_of_bags*float(flight['bag_price'])) for flight in trip]),
                        "travel_time": str(sum([(datetime.strptime(flight['arrival'], 
                                        '%Y-%m-%dT%H:%M:%S')-datetime.strptime(flight['departure'], 
                                        '%Y-%m-%dT%H:%M:%S')) for flight in trip], timedelta()))}
            json_output.append(json_object)
        
        #We are sorting dictionaries per trip by total price
        json_sorted_list = sorted(json_output, key= lambda x: x['total_price'])  # x['travel_time'], -x['bags_allowed']
        #Convert all data to string in JSON format
        return json.dumps(json_sorted_list, indent=4)  
    

    

if __name__ == "__main__":
    # print("Input:", conditions)
    search = Search(conditions)
    all_routes = search.flights_with_landings() + search.no_landings_between_flights()
    output = search.convert_to_json(all_routes)
    save(output)
    print(output)



    

    