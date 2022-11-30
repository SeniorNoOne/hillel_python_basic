from uuid import uuid4
from random import choice
from datetime import datetime
from tabulate import tabulate
from collections import namedtuple

Ticket = namedtuple("Ticket", ["id", "seat_num", "uuid4"])
Route = namedtuple("Route", ["id", "datetime", "route", "max_seats"])
ticket_header = ("ID", "Seat Number", "Control Code")
route_header = ("ID", "Date and Time", "Route", "Available tickets")

sold_tickets = []
routes = [
    Route(0, datetime.strptime("2022-12-10, 08:00", "%Y-%m-%d, %H:%M"),
          'Zhashkiv-Odesa', 38),
    Route(1, datetime.strptime("2022-12-10, 10:00", "%Y-%m-%d, %H:%M"),
          'Zhashkiv-Odesa', 40),
    Route(2, datetime.strptime("2022-12-10, 12:00", "%Y-%m-%d, %H:%M"),
          'Zhashkiv-Odesa', 42),
    Route(3, datetime.strptime("2022-11-10, 14:00", "%Y-%m-%d, %H:%M"),
          'Zhashkiv-Odesa', 28),
    Route(4, datetime.strptime("2022-11-10, 16:00", "%Y-%m-%d, %H:%M"),
          'Zhashkiv-Kyiv', 41),
    Route(5, datetime.strptime("2022-12-10, 18:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Kyiv", 40),
    Route(6, datetime.strptime("2022-12-10, 20:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Kyiv", 38),
    Route(7, datetime.strptime("2022-11-10, 22:00", "%Y-%m-%d, %H:%M"),
          "Zhashkiv-Kyiv", 35),
    Route(8, datetime.strptime("2022-12-10, 08:00", "%Y-%m-%d, %H:%M"),
          'Zhashkiv-Poltava', 40),
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


def buy_tickets(route: Route, amount_to_buy: int, _sold_tickets: list,
                _table_header: tuple = ticket_header) -> None:
    sold_tickets_by_id = filter_tickets_by_id(route.id, _sold_tickets)
    sold_seats_by_id = [ticket.seat_num for ticket in sold_tickets_by_id]
    available_seats_num = []
    max_seats_num = route.max_seats

    for seat_num in range(1, max_seats_num + 1):
        if seat_num not in sold_seats_by_id:
            available_seats_num.append(seat_num)

    sold_just_now_tickets = []
    if amount_to_buy <= max_seats_num - len(sold_seats_by_id):
        for index in range(amount_to_buy):
            sold_just_now_tickets.append(
                Ticket(route.id, available_seats_num[index], str(uuid4())))
        show_table(sold_just_now_tickets, _table_header)
        _sold_tickets.extend(sold_just_now_tickets)
    else:
        print("Sorry. We don't have enough tickets for you")


def subtract_sold_tickets(_routes: list, _sold_tickets: list) -> list:
    routes_without_sold_tickets = []
    for route in _routes:
        new_route = Route(route.id, route.datetime, route.route,
                          route.max_seats -
                          len(filter_tickets_by_id(route.id, _sold_tickets)))
        routes_without_sold_tickets.append(new_route)
    return routes_without_sold_tickets


def buy_tickets_input(_routes: list, _sold_tickets: list,
                      _table_header: tuple) -> None:
    print_routes = input("Show routes before buying (1 - yes)?: ")
    if print_routes == "1":
        show_table(_routes, _table_header)

    city_name = input("Enter city name where you want to go: ")
    city_name = city_name.strip().capitalize()
    routes_by_city_name = filter_routes_by_city_name(city_name, _routes)
    routes_without_sold_tickets = subtract_sold_tickets(routes_by_city_name,
                                                        _sold_tickets)

    if not routes_without_sold_tickets:
        print("Sorry. It seems you entered wrong city name")
    else:
        show_table(routes_without_sold_tickets, _table_header)
        route_id = int(input(f"Enter ID of the route you are interested in: "))
        route_by_id_and_city_name = filter_routes_by_id(route_id,
                                                        routes_by_city_name)
        if not route_by_id_and_city_name:
            print("Sorry. It seems you entered wrong route ID")
        else:
            if datetime.now() < route_by_id_and_city_name[-1].datetime:
                amount_to_buy = int(
                    input("Amount of tickets you want to buy: "))
                buy_tickets(route_by_id_and_city_name[-1], amount_to_buy,
                            sold_tickets)
            else:
                print("Sorry, but this route has already left")


def buy_random_input(_routes: list, _sold_tickets: list,
                     _table_header: tuple) -> None:
    routes_id = [route.id for route in _routes]
    rand_id = choice(routes_id)
    amount_to_buy = int(input("Number of tickets you want to buy: "))
    target_route = None

    for route in _routes:
        if route.id == rand_id:
            target_route = route
            break
    buy_tickets(target_route, amount_to_buy, _sold_tickets)


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


def main():
    while True:
        inp = int(input("\nWhat to do (0-5): "))

        match inp:
            case 0:
                break
            case 1:
                print("Showing routes:")
                show_table(routes, route_header)
            case 2:
                print("Buying tickets")
                buy_tickets_input(routes, sold_tickets, route_header)
            case 3:
                print("Trying to free ticket")
                free_ticket()
            case 4:
                print("Showing bought tickets")
                show_table(sold_tickets, ticket_header)
            case 5:
                print("Random route for you")
                buy_random_input(routes, sold_tickets, ticket_header)
            case _:
                print("Everything else")


if __name__ == "__main__":
    main()
