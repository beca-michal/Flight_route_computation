from datetime import datetime, timedelta


class Test():
    
    def is_time_correct(first_flight: dict, next_flight: dict):
        """Check whether the next flight will leave after the first arrive in between 1-6 hours

        Args:
            first (dict): First flight
            next (dict): Next flight

        Returns:
            Boolean
        """
        correct = (datetime.strptime(first_flight['arrival'], '%Y-%m-%dT%H:%M:%S') 
                            + timedelta(hours=1) <= datetime.strptime(next_flight['departure'], '%Y-%m-%dT%H:%M:%S')
                        and datetime.strptime(first_flight['arrival'], '%Y-%m-%dT%H:%M:%S') 
                            + timedelta(hours=6) >= datetime.strptime(next_flight['departure'], '%Y-%m-%dT%H:%M:%S'))
        # if not correct:
            # print(first['arrival'], next['departure'])
        return correct
        
    def is_time_in_trip_correct(trip: list):
        """Takes route as list of flights to detect 
        if every flight has correct arrival time before departure of next flight in between 1-6 hours
        Args:
            trip (list): list of flights in route
        Returns:
            Boolean: True if times in route are correct, Error if not
        """
        is_correct = True
        for first, next in zip(trip, trip[1:]):
            if not Test.is_time_correct(first, next):
                # raise ValueError
                return False
        
        return is_correct
    
    def counter(routes: list) -> dict:
        """Generate histogram of routes itineraries

        Args:
            routes (list): List of routes (flights to travel from origin to destination city)

        Returns:
            dict: Histogram of routes (Number of every unique itinerarie)
        """
        counter = {}
        for route in routes:
            itinerarie = (route[0]['origin'], *[flight['destination'] for flight in route])
                
            if not itinerarie in counter.keys():
                counter.update({itinerarie : 1})
            else:
                counter.update({itinerarie : counter[itinerarie] +1 })
            
        return counter
    
    def check_duplicates(routes: list) -> int:
        """Check if list of routes contains duplicates

        Args:
            routes (list): List of routes (flights to travel from origin to destination city)

        Returns:
            Integer: Number of duplicates
        """
        duplicates = 0
        duplicate_routes = list()
        for route in routes:
            if route in duplicate_routes:
                duplicates += 1
            else:
                duplicate_routes.append(route)
        return duplicates
    
    
    
                
                
        