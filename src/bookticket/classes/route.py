from datetime import datetime


class Route:
    def __init__(self, route_id: int, datetime_str: str,
                 direction: str, max_seats: int):
        self.id = route_id
        self.date_time = datetime.strptime(datetime_str, "%Y-%m-%d, %H:%M")
        self.direction = self.normalize_direction_string(direction)
        self.max_seats = max_seats
        self.available_seats = list(range(1, max_seats + 1))
        self.seat_ranges = []
        self.seat_ranges_str = ""
        # to correctly initialize seat_ranges and seat_ranges_str, we call
        # the callback method with empty list (means that we haven't sold
        # tickets yet)
        self.update_route([])

    def __str__(self):
        return f"ID: {self.id}, Datetime: {self.date_time}, " + \
               f"Direction: {self.direction}, " + \
               f"Max amount of seats: {self.max_seats}"

    def __repr__(self):
        return f"Route({self.id}, {self.date_time}, {self.direction,}" + \
               f"{self.max_seats})"

    def __iter__(self):
        # tabulate requires objects to be iterable to put them into table
        self._iterable = [self.id, self.date_time, self.direction,
                          self.max_seats]
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

    def show_available_seats(self) -> None:
        print(f"Available seats: {self.seat_ranges_str}")

    def update_route(self, sold_seats_num: list) -> None:
        available_seats = []
        for seat_num in self.available_seats:
            if seat_num not in sold_seats_num:
                available_seats.append(seat_num)
        self.max_seats -= len(sold_seats_num)
        self.available_seats = available_seats
        self.find_cont_intervals(available_seats)
        self.join_cont_intervals()


if __name__ == "__main__":
    route = Route(0, "2022-12-10, 08:00", "zhashkiv-odesa", 38)
    print(route)
