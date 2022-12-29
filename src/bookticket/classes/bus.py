from string import ascii_uppercase, digits
from random import choice
from src.bookticket.config import bus_number_format


class Bus:
    def __init__(self, bus_id: int, max_seats: int, bus_number=""):
        self.id = bus_id
        self.max_seats = max_seats
        self.bus_number = bus_number if bus_number else self.gen_plate_number()

    def __str__(self):
        return f"Number of seats: {self.max_seats}, " \
               f"Plate number: {self.bus_number}"

    def __repr__(self):
        return f"Bus({self.max_seats, self.bus_number})"

    @staticmethod
    def gen_plate_number():
        prefix = [choice(ascii_uppercase) for _ in
                  range(bus_number_format["prefix_len"])]
        numbers = [choice(digits) for _ in
                   range(bus_number_format["numbers_len"])]
        suffix = [choice(ascii_uppercase) for _ in
                  range(bus_number_format["suffix_len"])]
        return "".join(prefix + numbers + suffix)


if __name__ == "__main__":
    buses = [Bus(i, 30 + i) for i in range(3)]
    for bus in buses:
        print(bus)
