# datetime format string
datetime_format = "%Y-%m-%d, %H:%M"

# bus number format
bus_number_format = {"prefix_len": 2, "numbers_len": 4, "suffix_len": 2}

# CSV file headers
csv_headers = {"tickets": ["route_id", "sold_seat_num", "uuid"],
               "routes": ["date_time_str", "direction", "bus"],
               "buses": ["bus_id", "max_seats", "bus_number"]}

# file paths relative to classes folder
files_dir_cl = {"tickets": "../tickets.csv",
                "routes": "../routes.csv",
                "buses": "../buses.csv"}

# file paths relative to main.py
files_dir_main = {"tickets": "./tickets.csv",
                  "routes": "./routes.csv",
                  "buses": "./buses.csv"}

# file paths relative to test.py
files_dir_test = {"tickets": "./bookticket/tickets.csv",
                  "routes": "./bookticket/routes.csv",
                  "buses": "./bookticket/buses.csv"}

