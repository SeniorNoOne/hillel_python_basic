from uuid import uuid4


class Ticket:
    def __init__(self, route_id: int, sold_seat_num: int, uuid: str = ""):
        self.route_id = route_id
        self.sold_seat_num = sold_seat_num
        self.uuid = uuid if uuid else str(uuid4())

    def __str__(self):
        return f"ID: {self.route_id}, Sold seat number: {self.sold_seat_num}," \
               + f" UUID: {self.uuid}"

    def __repr__(self):
        return f"Ticket({self.route_id}, {self.sold_seat_num}, {self.uuid})"

    def __iter__(self):
        # tabulate requires objects to be iterable to put them into table
        iterable = [self.route_id, self.sold_seat_num, self.uuid]
        return iter(iterable)


if __name__ == "__main__":
    ticket = Ticket(0, 10)
    print(ticket)
