from datetime import datetime
from src.bookticket.config import datetime_format
from src.bookticket.classes.bus import Bus


class Route:
    def __init__(self, route_id: int, date_time_str: str,
                 direction: str, bus: Bus, sold_seats: list = ()):
        # provided parameters
        self.id = route_id
        self.bus = bus
        self.date_time = datetime.strptime(date_time_str, datetime_format)
        self.date_time_str = self.date_time.strftime(datetime_format)
        self.direction = ""

        # calculated parameters
        self.available_seats = [num for num in range(1, self.bus.max_seats + 1)]
        self.available_seats_left = len(self.available_seats)
        self.seat_ranges = []
        self.seat_ranges_str = ""
        self.normalize_direction_string(direction)
        # to correctly initialize seat_ranges and seat_ranges_str, we call
        # the callback method with empty list (means that we haven't sold
        # tickets yet)
        self.update_route(list(sold_seats))

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
                          self.available_seats_left]
        return iter(self._iterable)

    def normalize_direction_string(self, direction: str):
        if "-" in direction:
            start, end = direction.split("-")
            self.direction = start.capitalize() + "-" + end.capitalize()
        else:
            raise ValueError(f"Wrong direction format: {direction}")

    def show_available_seats(self) -> None:
        print(f"Available seats: {self.seat_ranges_str}")

    def update_route(self, sold_seats: list) -> None:
        available_seats = []
        for seat_num in self.available_seats:
            if seat_num not in sold_seats:
                available_seats.append(seat_num)
        self.available_seats = available_seats
        self.available_seats_left -= len(sold_seats)
        self.find_cont_intervals(available_seats)
        self.join_cont_intervals()

    def find_cont_intervals(self, seq: list) -> None:
        # not empty seq means that we have some available seats, so it's
        # possible to find continuous interval in this seq
        if seq:
            found_intervals = []
            subseq_len = 1
            subseq_start = seq[0]
            for index in range(1, len(seq)):
                if seq[index] - seq[index - 1] != 1:
                    found_intervals.append((subseq_start, subseq_len))
                    subseq_len = 1
                    subseq_start = seq[index]
                else:
                    subseq_len += 1
            found_intervals.append((subseq_start, subseq_len))
            self.seat_ranges = found_intervals
        # otherwise there are no available seats, so seat_ranges must be empty
        else:
            self.seat_ranges = []

    def join_cont_intervals(self) -> None:
        string = ""
        for start, subseq_len in self.seat_ranges:
            if subseq_len == 1:
                string += f"{start}, "
            else:
                string += f"{start}-{start + subseq_len - 1}, "
        string = string.rstrip(", ")
        self.seat_ranges_str = string if string else "No tickets left"


if __name__ == "__main__":
    bus1 = Bus(0, 40)
    route = Route(0, "2022-12-10, 08:00", "zhashkiv-odesa", bus1)
    print(route)
