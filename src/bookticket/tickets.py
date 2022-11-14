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


def show_routes():
    pass


def buy_ticket():
    pass


def free_ticket():
    pass


def main():
    while True:
        inp = int(input("What to do: "))

        match inp:
            case 0:
                break
            case 1:
                print("Showing routes\n")
                show_routes()
            case 2:
                print("Buying ticket\n")
                buy_ticket()
            case 3:
                print("Trying to free ticket\n")
                free_ticket()
            case _:
                print("Everything else\n")


if __name__ == "__main__":
    main()
