from config import files_dir_main
from src.bookticket.classes.bus_station import BusStation
from src.bookticket.classes.custom_exeptions import CSVHandlerError, TicketError


def main(bus_station):
    while True:
        inp = input("\nWhat to do (0-4): ").strip()

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
                    print("Showing bought tickets")
                    bus_station.show_table(table_type="ticket")
                case "4":
                    print("Random route for you")
                    bus_station.buy_random_input()
                case _:
                    print("Everything else")
        except (TicketError, CSVHandlerError, ValueError) as ex:
            print(ex)


if __name__ == "__main__":
    cass = BusStation(files_dir_main)
    with cass:
        main(cass)
