from src.bookticket.classes.custom_exeptions import TicketError
from src.bookticket.classes.ticket import Ticket
from src.bookticket.classes.route import Route
from tabulate import tabulate
from datetime import datetime, timedelta
from random import choice
from copy import deepcopy


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

    def __init__(self, routes: list = ()):
        if routes:
            self.routes = list(routes)
        else:
            self.routes = []
        self.tickets = []
        self.max_id = 0

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

    def append(self, *route_params) -> None:
        new_route = Route(self.max_id, *route_params)
        self.routes.append(new_route)
        self.max_id += 1
        self.update_outdated_route(new_route)

    def filter_tickets_by_id(self, route_id: int) -> list:
        tickets_by_id = []
        for ticket in self.tickets:
            if ticket.id == route_id:
                tickets_by_id.append(ticket)
        return tickets_by_id

    @staticmethod
    def filter_routes_by_id(route_id: int, routes: list) -> list:
        available_routes_by_id = []
        for route in routes:
            if route.bus.available_seats and route.id == route_id:
                available_routes_by_id.append(route)
        return available_routes_by_id

    @staticmethod
    def filter_routes_by_city_name(city_name: str, routes: list) -> list:
        available_routes_by_city_name = []
        for route in routes:
            destination_city = route.direction.split("-")[-1]
            if route.bus.available_seats and destination_city == city_name:
                available_routes_by_city_name.append(route)
        return available_routes_by_city_name

    @staticmethod
    def update_route(route_to_update: Route, just_sold_tickets: list) -> None:
        sold_seats_num = [ticket.sold_seat_num for ticket in just_sold_tickets]
        route_to_update.update_route(sold_seats_num)

    @staticmethod
    def find_seats_num_to_buy(amount_to_buy, route: Route) -> list:
        seat_ranges = sorted(route.bus.seat_ranges,
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
        if route.date_time < current_datetime:
            new_date = current_datetime + timedelta(days=7)
            new_date = new_date.replace(hour=route.date_time.hour,
                                        minute=route.date_time.minute,
                                        second=0, microsecond=0)
            new_route = Route(self.max_id, new_date.strftime("%Y-%m-%d, %H:%M"),
                              route.direction, deepcopy(route.bus))
            self.routes.append(new_route)
            self.max_id += 1

    def buy_tickets(self, route: Route, seats_num_to_buy: list) -> None:
        sold_just_now_tickets = []
        for seat_num in seats_num_to_buy:
            sold_just_now_tickets.append(Ticket(route.id, seat_num))
        self.show_table(sold_just_now_tickets, table_type="ticket")
        self.tickets.extend(sold_just_now_tickets)
        # callback function to update route's available seats
        self.update_route(route, sold_just_now_tickets)

    def free_tickets(self):
        pass

    def seats_num_input(self, route: Route) -> list:
        available_seats = route.bus.available_seats
        amount_to_buy = input("Number of tickets to buy: ").split(",")
        seats_num_to_buy = []

        if len(amount_to_buy) == 1:
            amount_to_buy = int(amount_to_buy[-1])
            if amount_to_buy <= route.bus.max_seats:
                seats_num_to_buy = self.find_seats_num_to_buy(amount_to_buy,
                                                              route)
        else:
            amount_to_buy = [int(seat_num) for seat_num in amount_to_buy if
                             seat_num.strip().isdecimal()]
            # using dict.fromkeys to remove duplicates and preserve order
            amount_to_buy = [*dict.fromkeys(amount_to_buy)]
            if all([seat_num in available_seats for seat_num in amount_to_buy]):
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
            if route.bus.available_seats and current_date < route.date_time:
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
    cassa = BusStation()
    cassa.append(("2022-12-22, 08:00", "Kyiv-Odesa", 20))
    cassa.append(("2022-12-22, 09:00", "Kyiv-Odesa", 20))
    cassa.append(("2022-12-22, 10:00", "Kyiv-Odesa", 20))
    print(cassa)
    print(id(cassa))

    new_cassa = BusStation()
    print(id(new_cassa))
