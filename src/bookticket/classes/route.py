from datetime import datetime


class Route:
    def __init__(self, route_id: int, datetime_str: str,
                 direction: str, max_seats: int):
        self.id = route_id
        self.date_time = datetime.strptime(datetime_str, "%Y-%m-%d, %H:%M")
        self.direction = self.normalize_direction_string(direction)
        self.max_seats = max_seats
        self.available_seats = list(range(1, max_seats + 1))

    def __str__(self):
        return f"ID: {self.id}, Datetime: {self.date_time}, " + \
               f"Direction: {self.direction}, " + \
               f"Max amount of seats: {self.max_seats}"

    def __repr__(self):
        return f"Route({self.id}, {self.date_time}, {self.direction,}" + \
               f"{self.max_seats})"

    def __iter__(self):
        # tabulate requires objects to be iterable to put them into table
        iterable = [self.id, self.date_time, self.direction, self.max_seats]
        return iter(iterable)

    @staticmethod
    def normalize_direction_string(direction: str):
        if "-" in direction:
            start, end = direction.split("-")
            return start.capitalize() + "-" + end.capitalize()
        else:
            print("Wrong direction format")


if __name__ == "__main__":
    route = Route(0, "2022-12-10, 08:00", "zhashkiv-odesa", 38)
    print(route)
