from src.bookticket.classes.bus_station import BusStation

routes = [
    (0, "2022-12-22, 08:00", "Zhashkiv-Odesa", 20),
    (1, "2022-12-22, 10:00", "Zhashkiv-Odesa", 40),
    (2, "2022-12-22, 12:00", "Zhashkiv-Odesa", 42),
    (3, "2022-12-10, 14:00", "Zhashkiv-Odesa", 28),
    (4, "2022-12-23, 16:00", "Zhashkiv-Kyiv", 41),
    (5, "2022-12-23, 18:00", "Zhashkiv-Kyiv", 40),
    (6, "2022-12-23, 20:00", "Zhashkiv-Kyiv", 38),
    (7, "2022-12-10, 22:00", "Zhashkiv-Kyiv", 35),
    (8, "2022-12-25, 08:00", "Zhashkiv-Poltava", 40),
    (9,  "2022-12-25, 10:00", "Zhashkiv-Poltava", 44),
    (10, "2022-12-25, 12:00", "Zhashkiv-Poltava", 38),
    (12, "2022-12-25, 14:00", "Zhashkiv-Poltava", 45),
    (13, "2022-12-11, 16:00", "Zhashkiv-Poltava", 37),
    (14, "2022-12-26, 06:00", "Zhashkiv-Lviv", 45),
    (15, "2022-12-26, 10:00", "Zhashkiv-Lviv", 43),
    (16, "2022-12-26, 16:00", "Zhashkiv-Lviv", 51),
    (17, "2022-12-11, 20:00", "Zhashkiv-Lviv", 33),
    (18, "2022-12-27, 8:00", "Zhashkiv-Uman", 25),
    (19, "2022-12-27, 10:00", "Zhashkiv-Uman", 35),
    (20, "2022-12-12, 12:00", "Zhashkiv-Uman", 28)
]


def main(bus_station):
    while True:
        inp = input("\nWhat to do (0-5): ").strip()

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

            case "4":
                print("Showing bought tickets")
                bus_station.show_table(header="ticket")
            case "5":
                print("Random route for you")
                bus_station.buy_random_input()
            case _:
                print("Everything else")


if __name__ == "__main__":
    cass = BusStation()
    for route in routes:
        cass.append(route)
    main(cass)
