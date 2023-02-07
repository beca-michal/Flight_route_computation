from datetime import datetime, timedelta

class Filters:
    """Class with filter methods used on lists
    """
    def __init__(self, conditions) -> None:
        self.origin = conditions['origin']
        self.destination = conditions['destination'] 
        self.number_of_bags = conditions['bags']
        self.return_path = conditions['return']    
        self.days_away = conditions['days_away']
        self.max_landings = conditions['max_landings']         
        pass
    
    def filter_by_bags(self, list_of_flights: list) -> list:
        """From input take number of bags and filter inserted list of flights, 
        to have the same or more bags allowed

        Args:
            list_of_flights (list): List of flights we want to apply fliter on

        Returns:
            list: Filtered list of flights
        """
        return [dict(flight) for flight in list_of_flights if self.number_of_bags <= int(flight['bags_allowed'])]
    
    def filter_direct_flights_by_cities(self, list_of_flights: list, origin: str, destination: str) -> list:
        """From list of flights take all flights that travel from origin to destination

        Args:
            list_of_flights (list): List of flights we want to apply fliter on
            origin (str): Shortcut for city in origin position
            destination (str): Shortcut for city in destination position

        Returns:
            list: Filtered list of flights
        """
        return [dict(flight) for flight in list_of_flights if (origin in flight['origin'] 
                            and destination in flight['destination'])]
        
    def filter_by_time(self, time_arrival: str, list_of_flights: list, delay_days = False):
        """Filter all input flights (list_of_flights) tied to (time_arrival) in interval <1,6> hours after time_arrival

        Args:
            time_arrival (_type_): String in specific format to mark arrival time
            list_of_flights (_type_): List of flights we want to apply fliter on
            delay_days (bool, optional): If True, we delay flights from destination by days from Input of program --days_away

        Returns:
            _type_: Filtered list of flights, which are tied to inserted time_arrival
        """
        if not delay_days:              
            return [dict(flight) for flight in list_of_flights 
                    if (datetime.strptime(time_arrival, '%Y-%m-%dT%H:%M:%S') 
                        + timedelta(hours=1) <= datetime.strptime(flight['departure'], '%Y-%m-%dT%H:%M:%S')
                    and datetime.strptime(time_arrival, '%Y-%m-%dT%H:%M:%S') 
                        + timedelta(hours=6) >= datetime.strptime(flight['departure'], '%Y-%m-%dT%H:%M:%S'))
                    ]
        else:
            delay_days = timedelta(days=self.days_away)
            return [dict(flight) for flight in list_of_flights 
                    if datetime.strptime(time_arrival, '%Y-%m-%dT%H:%M:%S') 
                        + delay_days <= datetime.strptime(flight['departure'], '%Y-%m-%dT%H:%M:%S')
                    ]
            

            
