from datetime import datetime, timedelta
from random import choice
from tabulate import tabulate
from src.bookticket.classes.bus import Bus
from src.bookticket.classes.csvhandler import CSVHandler, CSVReaderWriter
from src.bookticket.classes.custom_exeptions import TicketError
from src.bookticket.classes.route import Route
from src.bookticket.classes.ticket import Ticket
from src.bookticket.config import files_dir_cl, csv_headers, datetime_format


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BusStation(metaclass=SingletonMeta):
    headers = {"ticket": ("ID", "Seat Number", "Control Code"),
               "route": ("ID", "Date and Time", "Route", "Available tickets")}

    def __init__(self, file_paths: dict):
        # creating CSV factory object and opening required CSV files
        self.csv_factory = CSVHandler()
        self.routes_csv = self.csv_factory(file_paths["routes"],
                                           csv_headers["routes"], "rw")
        self.tickets_csv = self.csv_factory(file_paths["tickets"],
                                            csv_headers["tickets"], "rw")
        self.buses_csv = self.csv_factory(file_paths["buses"],
                                          csv_headers["buses"], "r")

        # initializing required variables
        self.max_id = 0
        self.tickets = []
        self.buses = []
        self.routes = []

        # reading data from files and putting processed data into variables
        self.read_from_csv_file(self.tickets_csv, self.init_ticket)
        self.read_from_csv_file(self.buses_csv, self.init_bus)
        self.read_from_csv_file(self.routes_csv, self.init_route)

    def __str__(self) -> str:
        routes_str = ""
        for route in self.routes:
            routes_str = routes_str + str(route) + "\n"
        return routes_str

    def __repr__(self) -> str:
        routes_str = ""
        for route in self.routes:
            routes_str = routes_str + repr(route) + "\n"
        return routes_str

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tickets_csv.close()
        self.routes_csv.close()
        self.buses_csv.close()

    def init_ticket(self, tickets_params: dict) -> None:
        self.tickets.append(Ticket(**tickets_params))

    def init_bus(self, bus_params: dict) -> None:
        self.buses.append(Bus(**bus_params))

    def init_route(self, route_params: dict) -> None:
        # replacing bus id with Bus instance
        route_params["bus"] = self.buses[route_params["bus"]]
        # taking into account already sold tickets from CSV file
        sold_tickets = self.filter_tickets_by_id(self.max_id)
        sold_seats = [ticket.sold_seat_num for ticket in sold_tickets]
        new_route = Route(self.max_id, **route_params, sold_seats=sold_seats)
        self.max_id += 1
        self.routes.append(new_route)
        # now we check if new_route is outdated and add another one if so
        self.update_outdated_route(new_route)

    def filter_tickets_by_id(self, route_id: int) -> list:
        tickets_by_id = []
        for ticket in self.tickets:
            if ticket.route_id == route_id:
                tickets_by_id.append(ticket)
        return tickets_by_id

    @staticmethod
    def filter_routes_by_id(route_id: int, routes: list) -> list:
        available_routes_by_id = []
        for route in routes:
            if route.available_seats and route.id == route_id:
                available_routes_by_id.append(route)
        return available_routes_by_id

    @staticmethod
    def filter_routes_by_city_name(city_name: str, routes: list) -> list:
        available_routes_by_city_name = []
        for route in routes:
            destination_city = route.direction.split("-")[-1]
            if route.available_seats and destination_city == city_name:
                available_routes_by_city_name.append(route)
        return available_routes_by_city_name

    @staticmethod
    def read_from_csv_file(csv_file: CSVReaderWriter, processing_method):
        for row in csv_file:
            row = {key: int(row[key]) if row[key].isdigit() else row[key]
                   for key in row}
            processing_method(row)

    @staticmethod
    def get_obj_param_by_name(obj, param_names: list) -> dict:
        return {key: obj.__dict__[key] for key in param_names}

    @staticmethod
    def find_seats_num_to_buy(amount_to_buy, route: Route) -> list:
        seat_ranges = sorted(route.seat_ranges,
                             key=lambda subseq: abs(subseq[-1] - amount_to_buy))
        seats_num_to_buy = []
        for start, subseq_len in seat_ranges:
            seats_num_to_buy.extend(list(range(start, start + subseq_len)))
            if len(seats_num_to_buy) >= amount_to_buy:
                break
        return seats_num_to_buy[:amount_to_buy]

    def show_table(self, table_to_show: list = (),
                   table_type: str = "route") -> None:
        if table_type == "route":
            table_to_show = table_to_show or self.routes
        else:
            table_to_show = table_to_show or self.tickets
        table_type = self.headers[table_type]
        table = tabulate(table_to_show, table_type, tablefmt="simple_outline")
        print(table)

    def update_outdated_route(self, route):
        current_datetime = datetime.now()
        # if current route is outdated we create new one with new datetime
        if route.date_time < current_datetime:
            new_date = current_datetime + timedelta(days=7)
            new_date = new_date.replace(hour=route.date_time.hour,
                                        minute=route.date_time.minute,
                                        second=0, microsecond=0)
            new_route = Route(self.max_id, new_date.strftime(datetime_format),
                              route.direction, route.bus)

            # now we check if new_route is in cvs file with routes
            # to do this we replace Bus instance with its id
            new_route_params = self.get_obj_param_by_name(new_route,
                                                          csv_headers["routes"])
            new_route_params["bus"] = str(new_route_params["bus"].id)
            # if new_route not in csv file we add it in file and list
            if new_route_params not in self.routes_csv.csv_data:
                self.max_id += 1
                self.routes.append(new_route)
                self.routes_csv.write_row(new_route_params)

    def buy_tickets(self, route: Route, seats_num_to_buy: list) -> None:
        sold_just_now_tickets = []
        for seat_num in seats_num_to_buy:
            ticket = Ticket(route.id, seat_num)
            sold_just_now_tickets.append(ticket)
            row_to_write = self.get_obj_param_by_name(ticket,
                                                      csv_headers["tickets"])
            self.tickets_csv.write_row(row_to_write)

        self.show_table(sold_just_now_tickets, table_type="ticket")
        self.tickets.extend(sold_just_now_tickets)
        # callback function to update route's available seats
        route.update_route([ticket.sold_seat_num for ticket in
                            sold_just_now_tickets])

    def seats_num_input(self, route: Route) -> list:
        amount_to_buy = input("Number of tickets to buy: ").split(",")
        seats_num_to_buy = []

        if len(amount_to_buy) == 1:
            amount_to_buy = int(amount_to_buy[-1])
            if amount_to_buy <= route.available_seats_left:
                seats_num_to_buy = self.find_seats_num_to_buy(amount_to_buy,
                                                              route)
        else:
            amount_to_buy = [int(seat_num) for seat_num in amount_to_buy if
                             seat_num.strip().isdecimal()]
            # using dict.fromkeys to remove duplicates and preserve order
            amount_to_buy = [*dict.fromkeys(amount_to_buy)]
            if all([seat_num in route.available_seats for seat_num in
                    amount_to_buy]):
                seats_num_to_buy.extend(amount_to_buy)
        return seats_num_to_buy

    def buy_tickets_input(self) -> None:
        if input("Show routes before buying (1 - yes)?: ") == "1":
            self.show_table()
        city_name = input("Enter city name where you want to go: ")
        city_name = city_name.strip().capitalize()
        filtered_routes = self.filter_routes_by_city_name(city_name,
                                                          self.routes)

        if filtered_routes:
            self.show_table(filtered_routes)
            route_id = int(input(f"Enter ID of the route you are "
                                 f"interested in: "))
            route = self.filter_routes_by_id(route_id, filtered_routes)
            if route:
                # filtering by city_name and id gives us a list with a single
                # route, so we unpack it
                route = route[-1]
                if datetime.now() < route.date_time:
                    route.show_available_seats()
                    if seats_num_to_buy := self.seats_num_input(route):
                        self.buy_tickets(route, seats_num_to_buy)
                    else:
                        raise TicketError("Sorry, it seems you are trying to "
                                          "buy already sold tickets or there "
                                          "are not enough tickets for you")
                else:
                    raise TicketError("Sorry, but this route has already left")
            else:
                raise TicketError("Sorry, it seems you entered wrong route ID")
        else:
            raise TicketError("Sorry, it seems you entered wrong city name")

    def buy_random_input(self) -> None:
        # not taking into account routes that has no seats left or already left
        current_date = datetime.now()
        filtered_routes = []
        for route in self.routes:
            if route.available_seats and current_date < route.date_time:
                filtered_routes.append(route)

        if filtered_routes:
            rand_route = choice(filtered_routes)
            rand_route.show_available_seats()
            if seats_num_to_buy := self.seats_num_input(rand_route):
                self.buy_tickets(rand_route, seats_num_to_buy)
            else:
                raise TicketError("Sorry, we don't have enough tickets for you")
        else:
            raise TicketError("Sorry, all the routes has left or all "
                              "tickets are sold")


if __name__ == "__main__":
    with BusStation(files_dir_cl) as cassa:
        pass
