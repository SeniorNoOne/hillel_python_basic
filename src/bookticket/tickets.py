from uuid import uuid4
from random import choice
from datetime import datetime
from tabulate import tabulate
from collections import namedtuple

Ticket = namedtuple("Ticket", ["id", "seat_num", "uuid4"])
Route = namedtuple("Route", ["id", "date_time", "route", "max_seats"])
ticket_header = ("ID", "Seat Number", "Control Code")
route_header = ("ID", "Date and Time", "Route", "Available tickets")

sold_tickets = []
routes = [
    Route(0, datetime.strptime("2022-12-10, 08:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Odesa", 38),
    Route(1, datetime.strptime("2022-12-10, 10:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Odesa", 40),
    Route(2, datetime.strptime("2022-12-10, 12:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Odesa", 42),
    Route(3, datetime.strptime("2022-11-10, 14:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Odesa", 28),
    Route(4, datetime.strptime("2022-11-10, 16:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Kyiv", 41),
    Route(5, datetime.strptime("2022-12-10, 18:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Kyiv", 40),
    Route(6, datetime.strptime("2022-12-10, 20:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Kyiv", 38),
    Route(7, datetime.strptime("2022-11-10, 22:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Kyiv", 35),
    Route(8, datetime.strptime("2022-12-10, 08:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Poltava", 40),
    Route(9,  datetime.strptime("2022-12-10, 10:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Poltava", 44),
    Route(10, datetime.strptime("2022-11-11, 12:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Poltava", 38),
    Route(12, datetime.strptime("2022-12-12, 14:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Poltava", 45),
    Route(13, datetime.strptime("2022-11-12, 16:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Poltava", 37),
    Route(14, datetime.strptime("2022-12-12, 06:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Lviv", 45),
    Route(15, datetime.strptime("2022-11-12, 10:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Lviv", 43),
    Route(16, datetime.strptime("2022-12-12, 16:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Lviv", 51),
    Route(17, datetime.strptime("2022-12-12, 20:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Lviv", 33),
    Route(18, datetime.strptime("2022-11-12, 8:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Uman", 25),
    Route(19, datetime.strptime("2022-12-12, 10:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Uman", 35),
    Route(20, datetime.strptime("2022-12-12, 12:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Uman", 28)
]


def find_ascending_subseq(seq: list, subseq_len: int) -> list:
    found_subseq = []
    if seq:
        prev_item = seq[0]
        buff = [prev_item]
        for item in seq[1::]:
            if not buff or (item - prev_item) == 1:
                buff.append(item)
            else:
                buff = [item]
            if len(buff) == subseq_len:
                found_subseq.append(tuple(buff))
                buff = []
            prev_item = item
    return found_subseq


def find_cont_intervals(seq: list) -> list:
    found_intervals = []
    if seq:
        start = prev_item = seq[0]
        for item in seq[1::]:
            if not item - prev_item == 1:
                found_intervals.append((start, prev_item))
                start = item
            prev_item = item
        found_intervals.append((start, prev_item))
    return found_intervals


def join_cont_intervals(intervals: list) -> str:
    string = ""
    for start, end in intervals:
        if start == end:
            string += f"{start}, "
        else:
            string += f"{start}-{end}, "
    total_string = string.rstrip(", ")
    return total_string if total_string else "No tickets left"


def get_available_seats(route: Route, _sold_tickets) -> list:
    sold_tickets_by_id = filter_tickets_by_id(route.id, _sold_tickets)
    sold_seats_by_id = [ticket.seat_num for ticket in sold_tickets_by_id]
    available_seats_num = []
    for seat_num in range(1, route.max_seats + 1):
        if seat_num not in sold_seats_by_id:
            available_seats_num.append(seat_num)
    return available_seats_num


def buy_tickets(route: Route, seats_num_to_buy: list, _sold_tickets: list,
                _table_header: tuple = ticket_header) -> None:
    sold_just_now_tickets = []

    for seat_num in seats_num_to_buy:
        sold_just_now_tickets.append(Ticket(route.id, seat_num, str(uuid4())))
    show_table(sold_just_now_tickets, _table_header)
    _sold_tickets.extend(sold_just_now_tickets)


def subtract_sold_tickets(_routes: list, _sold_tickets: list) -> list:
    routes_without_sold_tickets = []
    for route in _routes:
        tickets_by_id = filter_tickets_by_id(route.id, _sold_tickets)
        route_without_sold_tickets = Route(route.id, route.date_time,
                                           route.route, route.max_seats -
                                           len(tickets_by_id))
        routes_without_sold_tickets.append(route_without_sold_tickets)
    return routes_without_sold_tickets


def seats_num_input(available_seats: list) -> list:
    amount_to_buy = input("Amount of tickets you want to buy: ").split(",")
    # using dict.fromkeys to remove duplicates and preserve order
    amount_to_buy = [*dict.fromkeys(amount_to_buy)]
    seats_to_buy = []

    if len(amount_to_buy) == 1:
        amount_to_buy = subseq_len = int(amount_to_buy[-1])

        while subseq_len:
            if buff := find_ascending_subseq(available_seats, subseq_len):
                if subseq_len * len(buff) >= amount_to_buy:
                    for item in buff:
                        seats_to_buy.extend(item)
                    seats_to_buy = seats_to_buy[:amount_to_buy]
                    break
            subseq_len -= 1
    else:
        amount_to_buy = [int(seat_num) for seat_num in amount_to_buy if
                         seat_num.strip().isdecimal()]
        if all([seat_num in available_seats for seat_num in amount_to_buy]):
            seats_to_buy.extend(amount_to_buy)
    return seats_to_buy


def buy_tickets_input(_routes: list, _sold_tickets: list,
                      _table_header: tuple = route_header) -> None:
    if input("Show routes before buying (1 - yes)?: ") == "1":
        show_table(subtract_sold_tickets(_routes, _sold_tickets), _table_header)

    city_name = input("Enter city name where you want to go: ")
    city_name = city_name.strip().capitalize()

    routes_by_city_name = filter_routes_by_city_name(city_name, _routes)
    routes_without_sold_tickets = subtract_sold_tickets(routes_by_city_name,
                                                        _sold_tickets)

    if routes_without_sold_tickets:
        show_table(routes_without_sold_tickets, _table_header)
        route_id = int(input(f"Enter ID of the route you are interested in: "))
        route_by_id_and_city_name = filter_routes_by_id(route_id,
                                                        routes_by_city_name)
        if route_by_id_and_city_name:
            route_by_id_and_city_name = route_by_id_and_city_name[-1]
            if datetime.now() < route_by_id_and_city_name.date_time:
                available_seats = get_available_seats(route_by_id_and_city_name,
                                                      sold_tickets)
                show_available_seats(available_seats)
                if seats_to_buy := seats_num_input(available_seats):
                    buy_tickets(route_by_id_and_city_name, seats_to_buy,
                                _sold_tickets)
                else:
                    print("Sorry, it seems you are trying to buy already sold",
                          "ticket or there are not enough tickets for you")
            else:
                print("Sorry, but this route has already left")
        else:
            print("Sorry, it seems you entered wrong route ID")
    else:
        print("Sorry, it seems you entered wrong city name")


def buy_random_input(_routes: list, _sold_tickets: list,
                     _table_header: tuple) -> None:
    # not taking into account routes that has no seats left or already left
    current_date = datetime.now()
    filtered_routes = []

    for route in subtract_sold_tickets(_routes, _sold_tickets):
        if current_date < route.date_time and route.max_seats:
            filtered_routes.append(route)

    [print(i) for i in filtered_routes]

    if filtered_routes:
        rand_route = choice(filtered_routes)
        available_seats = get_available_seats(rand_route, _sold_tickets)
        show_available_seats(available_seats)
        if seats_to_buy := seats_num_input(available_seats):
            buy_tickets(rand_route, seats_to_buy, _sold_tickets)
        else:
            print("Sorry, we don't have enough tickets for you")
    else:
        print("Sorry, all the routes has left or all tickets are sold")


def free_ticket():
    pass


def filter_tickets_by_id(_id: int, _sold_tickets: list) -> list:
    tickets_by_id = []
    for ticket in _sold_tickets:
        if ticket.id == _id:
            tickets_by_id.append(ticket)
    return tickets_by_id


def filter_routes_by_city_name(city_name: str, _routes: list) -> list:
    available_routes_by_city_name = []
    for route in _routes:
        destination_city = route.route.split("-")[-1]
        if destination_city == city_name:
            available_routes_by_city_name.append(route)
    return available_routes_by_city_name


def filter_routes_by_id(_id: int, _routes: list) -> list:
    available_routes_by_id = []
    for route in _routes:
        if route.id == _id:
            available_routes_by_id.append(route)
    return available_routes_by_id


def show_table(table_to_show: list, headers: tuple = None) -> None:
    if headers:
        table = tabulate(table_to_show, headers, tablefmt="simple_outline")
    else:
        table = tabulate(table_to_show, tablefmt="simple_outline")
    print(table)


def show_available_seats(available_seats: list) -> None:
    intervals = find_cont_intervals(available_seats)
    string = join_cont_intervals(intervals)
    print(f"Available seats: {string}")


def main():
    while True:
        inp = input("\nWhat to do (0-5): ").strip()

        match inp:
            case "0":
                break
            case "1":
                print("Showing routes:")
                show_table(subtract_sold_tickets(routes, sold_tickets),
                           route_header)
            case "2":
                print("Buying tickets")
                buy_tickets_input(routes, sold_tickets, route_header)
            case "3":
                print("Trying to free ticket")
                free_ticket()
            case "4":
                print("Showing bought tickets")
                show_table(sold_tickets, ticket_header)
            case "5":
                print("Random route for you")
                buy_random_input(routes, sold_tickets, ticket_header)
            case _:
                print("Everything else")


if __name__ == "__main__":
    main()
