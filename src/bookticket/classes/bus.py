import string
from random import choice


class Bus:
    def __init__(self, max_seats, number=""):
        self.max_seats = max_seats
        self.plate_number = number if number else self.gen_plate_number()
        self.available_seats = list(range(1, max_seats + 1))
        self.seat_ranges = []
        self.seat_ranges_str = ""
        self.update_bus([])

    def __str__(self):
        return f"Number of seats: {self.max_seats}, " \
               f"Plate number: {self.plate_number}, " \
               f"Available seats: {self.seat_ranges_str}"

    def __repr__(self):
        return f"Bus({self.max_seats, self.plate_number})"

    @staticmethod
    def gen_plate_number():
        prefix = [choice(string.ascii_uppercase) for _ in range(2)]
        numbers = [choice(string.digits) for _ in range(4)]
        suffix = [choice(string.ascii_uppercase) for _ in range(2)]
        return "".join(prefix + numbers + suffix)

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
        _string = ""
        for start, subseq_len in self.seat_ranges:
            if subseq_len == 1:
                _string += f"{start}, "
            else:
                _string += f"{start}-{start + subseq_len - 1}, "
        _string = _string.rstrip(", ")
        self.seat_ranges_str = _string if _string else "No tickets left"

    def show_available_seats(self) -> None:
        print(f"Available seats: {self.seat_ranges_str}")

    def update_bus(self, sold_seats_num: list) -> None:
        available_seats = []
        for seat_num in self.available_seats:
            if seat_num not in sold_seats_num:
                available_seats.append(seat_num)
        self.max_seats -= len(sold_seats_num)
        self.available_seats = available_seats
        self.find_cont_intervals(available_seats)
        self.join_cont_intervals()


if __name__ == "__main__":
    buses = [Bus(30 + i) for i in range(3)]
    for bus in buses:
        print(bus)
