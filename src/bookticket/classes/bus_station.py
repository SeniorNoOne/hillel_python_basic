from src.bookticket.classes.ticket import Ticket
from src.bookticket.classes.route import Route
from tabulate import tabulate
from datetime import datetime
from random import choice


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

    def validate_id(self, new_route):
        return all([new_route.id != route.id for route in self.routes])

    def append(self, route_params: tuple) -> None:
        new_route = Route(*route_params)
        if self.validate_id(new_route):
            self.routes.append(new_route)
        else:
            print("New route ID must be unique")

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
    def update_route(route_to_update: Route, just_sold_tickets: list) -> None:
        sold_seats_num = [ticket.sold_seat_num for ticket in just_sold_tickets]
        route_to_update.max_seats -= len(sold_seats_num)
        available_seats = []
        for seat_num in route_to_update.available_seats:
            if seat_num not in sold_seats_num:
                available_seats.append(seat_num)
        route_to_update.available_seats = available_seats

    @staticmethod
    def find_cont_intervals(seq: list) -> list:
        found_intervals = []
        subseq_len = 1
        subseq_start = seq[0]
        if seq:
            for index in range(1, len(seq)):
                if seq[index] - seq[index - 1] != 1:
                    found_intervals.append((subseq_start, subseq_len))
                    subseq_len = 1
                    subseq_start = seq[index]
                else:
                    subseq_len += 1
            found_intervals.append((subseq_start, subseq_len))
        return found_intervals

    @staticmethod
    def join_cont_intervals(intervals: list) -> str:
        string = ""
        for start, subseq_len in intervals:
            if subseq_len == 1:
                string += f"{start}, "
            else:
                string += f"{start}-{start + subseq_len - 1}, "
        total_string = string.rstrip(", ")
        return total_string if total_string else "No tickets left"

    def find_seats_num_to_buy(self, amount_to_buy, route: Route) -> list:
        intervals = self.find_cont_intervals(route.available_seats)
        intervals = sorted(intervals, key=lambda interval: interval[-1])
        seats_to_buy = []
        for start, subseq_len in intervals:
            # selling tickets from the best match (0 - exact match, bigger
            # than 1 - selling from bigger range)
            if subseq_len - amount_to_buy >= 0:
                seats_to_buy.extend(list(range(start, start + subseq_len)))
            if len(seats_to_buy) >= amount_to_buy:
                break
        seats_to_buy = seats_to_buy[0:amount_to_buy]
        return seats_to_buy

    def show_available_seats(self, route: Route) -> None:
        intervals = self.find_cont_intervals(route.available_seats)
        string = self.join_cont_intervals(intervals)
        print(f"Available seats: {string}")

    def show_table(self, table_to_show: list = (),
                   header: str = "route") -> None:
        if header == "route":
            table_to_show = table_to_show or self.routes
        else:
            table_to_show = table_to_show or self.tickets
        header = self.headers[header]
        table = tabulate(table_to_show, header, tablefmt="simple_outline")
        print(table)

    def buy_tickets(self, route: Route, seats_num_to_buy: list) -> None:
        sold_just_now_tickets = []
        for seat_num in seats_num_to_buy:
            sold_just_now_tickets.append(Ticket(route.id, seat_num))
        self.show_table(sold_just_now_tickets, header="ticket")
        self.tickets.extend(sold_just_now_tickets)
        # callback function to update route's available seats
        self.update_route(route, sold_just_now_tickets)

    def free_tickets(self):
        pass

    def seats_num_input(self, route: Route) -> list:
        available_seats = route.available_seats
        amount_to_buy = input("Amount of tickets you want to buy: ").split(",")
        # using dict.fromkeys to remove duplicates and preserve order
        amount_to_buy = [*dict.fromkeys(amount_to_buy)]
        seats_to_buy = []

        if len(amount_to_buy) == 1:
            amount_to_buy = int(amount_to_buy[-1])
            if amount_to_buy <= len(route.available_seats):
                seats_to_buy = self.find_seats_num_to_buy(amount_to_buy, route)
        else:
            amount_to_buy = [int(seat_num) for seat_num in amount_to_buy if
                             seat_num.strip().isdecimal()]
            if all([seat_num in available_seats for seat_num in amount_to_buy]):
                seats_to_buy.extend(amount_to_buy)
        return seats_to_buy

    def buy_tickets_input(self) -> None:
        if input("Show routes before buying (1 - yes)?: ") == "1":
            self.show_table(self.routes)

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
                route = route[-1]
                if datetime.now() < route.date_time:
                    self.show_available_seats(route)
                    if seats_to_buy := self.seats_num_input(route):
                        self.buy_tickets(route, seats_to_buy)
                    else:
                        print("Sorry, it seems you are trying to buy already "
                              "sold tickets or there are not enough tickets "
                              "for you")
                else:
                    print("Sorry, but this route has already left")
            else:
                print("Sorry, it seems you entered wrong route ID")
        else:
            print("Sorry, it seems you entered wrong city name")

    def buy_random_input(self) -> None:
        # not taking into account routes that has no seats left or already left
        current_date = datetime.now()
        filtered_routes = []
        for route in self.routes:
            if current_date < route.date_time and route.max_seats:
                filtered_routes.append(route)

        if filtered_routes:
            rand_route = choice(filtered_routes)
            self.show_available_seats(rand_route)
            if seats_to_buy := self.seats_num_input(rand_route):
                self.buy_tickets(rand_route, seats_to_buy)
            else:
                print("Sorry, we don't have enough tickets for you")
        else:
            print("Sorry, all the routes has left or all tickets are sold")


if __name__ == "__main__":
    cassa = BusStation()
    cassa.append((0, "2022-12-22, 08:00", "Kyiv-Odesa", 20))
    cassa.append((1, "2022-12-22, 09:00", "Kyiv-Odesa", 20))
    cassa.append((1, "2022-12-22, 10:00", "Kyiv-Odesa", 20))
    print(cassa)
    print(id(cassa))

    new_cassa = BusStation()
    print(id(new_cassa))
