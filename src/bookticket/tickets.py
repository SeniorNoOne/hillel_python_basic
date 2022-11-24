from uuid import uuid4
from random import choice

routes = [
    (0, '2022-11-10', '08:00', 'Zhashkiv-Odesa', 38),
    (1, '2022-11-10', '10:00', 'Zhashkiv-Odesa', 40),
    (2, '2022-11-10', '12:00', 'Zhashkiv-Odesa', 42),
    (3, '2022-11-10', '14:00', 'Zhashkiv-Odesa', 28),
    (4, '2022-11-10', '16:00', 'Zhashkiv-Kyiv', 41),
    (5, '2022-11-10', '18:00', 'Zhashkiv-Kyiv', 40),
    (6, '2022-11-10', '20:00', 'Zhashkiv-Kyiv', 38),
    (7, '2022-11-10', '22:00', 'Zhashkiv-Kyiv', 35),
    (8, '2022-11-10', '08:00', 'Zhashkiv-Poltava', 40),
    (9, '2022-11-10', '10:00', 'Zhashkiv-Poltava', 44),
    (10, '2022-11-11', '12:00', 'Zhashkiv-Poltava', 38),
    (12, '2022-11-12', '14:00', 'Zhashkiv-Poltava', 45),
    (13, '2022-11-12', '16:00', 'Zhashkiv-Poltava', 37),
    (14, '2022-11-12', '06:00', 'Zhashkiv-Lviv', 45),
    (15, '2022-11-12', '10:00', 'Zhashkiv-Lviv', 43),
    (16, '2022-11-12', '16:00', 'Zhashkiv-Lviv', 51),
    (17, '2022-11-12', '20:00', 'Zhashkiv-Lviv', 33),
    (18, '2022-11-12', '8:00', 'Zhashkiv-Uman', 25),
    (19, '2022-11-12', '10:00', 'Zhashkiv-Uman', 35),
    (20, '2022-11-12', '12:00', 'Zhashkiv-Uman', 28),
]


def buy_ticket(_sold_tickets: list, spacer: str = "") -> None:
    print_routes = input(f"{spacer}Show routes before buying (1 - yes)?: ")

    if print_routes == "1":
        show_routes(routes, spacer=2 * spacer)

    city_name = input(f"{spacer}Enter city name where you want to go: ")
    city_name = city_name.strip().capitalize()
    routes_by_city_name = get_available_routes_by(city_name, routes)
    routes_id_by_city_name = [route[0] for route in routes_by_city_name]

    if routes_id_by_city_name:
        print(f"{spacer}We have following routes for you: ")
        show_routes(routes_by_city_name, spacer=2 * spacer)
        route_id = int(input(f"{spacer}Enter ID of the route you "
                             f"are interested in: "))
        if route_id in routes_id_by_city_name:
            tickets_amount_to_buy = int(input(f"{spacer}Number of tickets "
                                              f"you want to buy: "))
            available_tickets = get_available_tickets_by(route_id,
                                                         _sold_tickets)

            if (len(available_tickets) - tickets_amount_to_buy) < 0:
                print(f"{spacer}Sorry, but we don't have enough tickets for you"
                      "or route with such ID doesn't exist")
            else:
                print(f"{spacer}Here are your tickets:")
                for index in range(0, tickets_amount_to_buy):
                    ticket = (route_id, available_tickets[index], str(uuid4()))
                    _sold_tickets.append(ticket)
                    print("{0}ID: {1}, Seat number: "
                          "{2}, Control: {3}".format(2 * spacer, *ticket))
        else:
            print(f"{spacer}Wrong input there is no route with such ID and "
                  f"destination city")
    else:
        print(f"{spacer}Wrong input. There is no such city in available routes")
    print()


def get_me_outta_of_here(available_routes: list,
                         _sold_tickets: list,
                         spacer="") -> None:
    routes_id = [route[0] for route in available_routes]
    rand_id = choice(routes_id)

    tickets_amount_to_buy = int(input(f"{spacer}Number of tickets "
                                      f"you want to buy: "))
    available_tickets = get_available_tickets_by(rand_id, _sold_tickets)

    if (len(available_tickets) - tickets_amount_to_buy) < 0:
        print(f"{spacer}Sorry, but we don't have enough tickets for you "
              "or route with such ID doesn't exist")
    else:
        print(f"{spacer}Here are your tickets:")
        for index in range(0, tickets_amount_to_buy):
            ticket = (rand_id, available_tickets[index], str(uuid4()))
            _sold_tickets.append(ticket)
            print("{0}ID: {1}, Seat number: "
                  "{2}, Control: {3}".format(2 * spacer, *ticket))
    print()


def free_ticket():
    pass


def get_available_tickets_by(_id: int, sold_tickets: list) -> list:
    available_tickets_by_id = []
    if len(routes) >= _id:
        max_tickets = routes[_id][-1]
        sold_seat_num_by_id = [ticket[1] for ticket in sold_tickets if
                               ticket[0] == _id]
        for ticket_num in range(1, max_tickets + 1):
            if ticket_num not in sold_seat_num_by_id:
                available_tickets_by_id.append(ticket_num)
    return available_tickets_by_id


def get_available_routes_by(city_name: str, available_routes: list) -> list:
    available_routes_by_city_name = []

    for route in available_routes:
        destination_city = route[3].split("-")[-1]
        if city_name in destination_city:
            available_routes_by_city_name.append(route)
    return available_routes_by_city_name


def show_sold_tickets(_sold_tickets: list, spacer: str = "") -> None:
    if len(_sold_tickets):
        for route_id, seat_num, control_str in _sold_tickets:
            print(f"{spacer}Route ID: {route_id}, Seat number: {seat_num}, "
                  f"Control string: {control_str}")
    else:
        print("There are no sold tickets yet")
    print()


def show_routes(routes_to_show, spacer: str = "") -> None:
    for route_id, date, time, route, max_tickets in routes_to_show:
        print(f"{spacer}Route ID: {route_id}, Date: {date}, Time: {time}",
              f"Route: {route}, Maximum number of tickets: {max_tickets}")
    print()


def main():
    sold_tickets = []

    while True:
        inp = int(input("What to do: "))

        match inp:
            case 0:
                break
            case 1:
                print("\nShowing routes:")
                show_routes(routes, spacer="\t")
            case 2:
                print("\nBuying ticket")
                buy_ticket(sold_tickets, spacer="\t")
            case 3:
                print("\nTrying to free ticket\n")
                free_ticket()
            case 4:
                print("\nShowing bought tickets")
                show_sold_tickets(sold_tickets, spacer="\t")
            case 5:
                print("\nRandom route for you")
                get_me_outta_of_here(routes, sold_tickets, spacer="\t")
            case _:
                print("\nEverything else")


if __name__ == "__main__":
    main()
