from src.bookticket.classes.bus_station import BusStation, TicketError
from src.bookticket.classes.bus import Bus
from random import randint, choice

busses = [Bus(30 + randint(-5, 10)) for i in range(15)]
routes = [
    ("2022-12-22, 08:00", "Zhashkiv-Odesa"),
    ("2022-12-22, 10:00", "Zhashkiv-Odesa"),
    ("2022-12-22, 12:00", "Zhashkiv-Odesa"),
    ("2022-12-10, 14:00", "Zhashkiv-Odesa"),
    ("2022-12-23, 16:00", "Zhashkiv-Kyiv"),
    ("2022-12-23, 18:00", "Zhashkiv-Kyiv"),
    ("2022-12-23, 20:00", "Zhashkiv-Kyiv"),
    ("2022-12-10, 22:00", "Zhashkiv-Kyiv"),
    ("2022-12-25, 08:00", "Zhashkiv-Poltava"),
    ("2022-12-25, 10:00", "Zhashkiv-Poltava"),
    ("2022-12-25, 12:00", "Zhashkiv-Poltava"),
    ("2022-12-25, 14:00", "Zhashkiv-Poltava"),
    ("2022-12-11, 16:00", "Zhashkiv-Poltava"),
    ("2022-12-26, 06:00", "Zhashkiv-Lviv"),
    ("2022-12-26, 10:00", "Zhashkiv-Lviv"),
    ("2022-12-26, 16:00", "Zhashkiv-Lviv"),
    ("2022-12-11, 20:00", "Zhashkiv-Lviv"),
    ("2022-12-27, 8:00", "Zhashkiv-Uman"),
    ("2022-12-27, 10:00", "Zhashkiv-Uman"),
    ("2022-12-12, 12:00", "Zhashkiv-Uman")
]


def main(bus_station):
    while True:
        inp = input("\nWhat to do (0-5): ").strip()

        try:
            match inp:
                case "0":
                    break
                case "1":
                    print("Showing routes:")
                    bus_station.show_table()
                case "2":
                    print("Buying tickets")
                    bus_station.buy_tickets_input()
                case "3":
                    print("Trying to free ticket")
                    bus_station.free_tickets()
                case "4":
                    print("Showing bought tickets")
                    bus_station.show_table(table_type="ticket")
                case "5":
                    print("Random route for you")
                    bus_station.buy_random_input()
                case "6":
                    bus_station.update_outdated_routes()
                case _:
                    print("Everything else")
        except TicketError as ex:
            print(ex)


if __name__ == "__main__":
    cass = BusStation()
    for route in routes:
        cass.append(*route, choice(busses))
    main(cass)
