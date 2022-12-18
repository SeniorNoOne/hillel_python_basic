from src.bookticket.classes.bus import Bus
from datetime import datetime


class Route:
    def __init__(self, route_id: int, datetime_str: str,
                 direction: str, bus: Bus):
        self.id = route_id
        self.date_time = datetime.strptime(datetime_str, "%Y-%m-%d, %H:%M")
        self.direction = self.normalize_direction_string(direction)
        self.bus = bus
        # to correctly initialize seat_ranges and seat_ranges_str, we call
        # the callback method with empty list (means that we haven't sold
        # tickets yet)
        self.update_route([])

    def __str__(self):
        return f"ID: {self.id}, Datetime: {self.date_time}, " + \
               f"Direction: {self.direction}, " + \
               f"Max amount of seats: {self.bus.max_seats}"

    def __repr__(self):
        return f"Route({self.id}, {self.date_time}, {self.direction}," + \
               f"{self.bus.max_seats})"

    def __iter__(self):
        # tabulate requires objects to be iterable to put them into table
        self._iterable = [self.id, self.date_time, self.direction,
                          self.bus.max_seats]
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._iterable):
            self._index += 1
            return self._iterable[self._index - 1]
        raise StopIteration

    @staticmethod
    def normalize_direction_string(direction: str):
        if "-" in direction:
            start, end = direction.split("-")
            return start.capitalize() + "-" + end.capitalize()
        else:
            print("Wrong direction format")

    def show_available_seats(self) -> None:
        print(f"Available seats: {self.bus.seat_ranges_str}")

    def update_route(self, sold_seats_num: list) -> None:
        self.bus.update_bus(sold_seats_num)


if __name__ == "__main__":
    bus1 = Bus(40)
    route = Route(0, "2022-12-10, 08:00", "zhashkiv-odesa", bus1)
    print(route)
