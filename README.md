# Python weekend entry task completed - Beca Michal

**Python script for a given flight data in a form of `csv` file, prints out a structured list of all flight combinations for a selected route between airports A -> B, sorted by the final price for the trip.**

### Arguments as input

| Argument name | type   | Description              | Notes |
| ------------- | ------ | ------------------------ | ----- |
| `csv_name`    | string | Name of csv file         |       |
| `origin`      | string | Origin airport code      |       |
| `destination` | string | Destination airport code |       |

### Optional arguments

| Argument name    | type    | Description              | Notes                        |
| ---------------- | ------- | ------------------------ | ---------------------------- |
| `--bags`         | integer | Number of requested bags | Optional (defaults to 0)     |
| `--return`       | boolean | Is it a return flight?   | Optional (defaults to false) |
| `--days_away`    | integer | Days before return       | Optional (defaults to 0)     |
| `--max_landings` | integer | Max number of landings   | Optional (defaults to 2)     |

### Starting script

All necessary calculations are in solution.py with accompaniment of filter.py
Script will start calculations after running solution.py following with necessary arguments
for more info about arguments type argument -h
INFO: python solution.py -h

### Examples for terminal to start script

python -m solution example/example0.csv RFZ WIW --bags=1 --return
python -m solution example1.csv SML DHE --bags=2 --return
python -m solution example2.csv IUT LOM --bags=1 --return --max_landings=3 --days_away=2

Input0: {'csv_name': 'example/example0.csv', 'origin': 'RFZ', 'destination': 'WIW', 'bags': 1, 'return': True, 'days_away': 0, 'max_landings': 2}
Input1: {'csv_name': 'example1.csv', 'origin': 'SML', 'destination': 'DHE', 'bags': 2, 'return': True, 'days_away': 0, 'max_landings': 2}
Input2: {'csv_name': 'example2.csv', 'origin': 'IUT', 'destination': 'LOM', 'bags': 1, 'return': True, 'days_away': 2, 'max_landings': 3}

### Output

The output will be a json-compatible structured list of trips sorted by price printed in terminal and saved to data.json file in main folder
