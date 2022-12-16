from uuid import uuid4


class Ticket:
    def __init__(self, route_id, sold_seat_num):
        self.id = route_id
        self.sold_seat_num = sold_seat_num
        self.uuid = str(uuid4())

    def __str__(self):
        return f"ID: {self.id}, Sold seat number: {self.sold_seat_num}," \
               + f" UUID: {self.uuid}"

    def __repr__(self):
        return f"Ticket({self.id}, {self.sold_seat_num}, {self.uuid})"

    def __iter__(self):
        # tabulate requires objects to be iterable to put them into table
        iterable = [self.id, self.sold_seat_num, self.uuid]
        return iter(iterable)


if __name__ == "__main__":
    ticket = Ticket(0, 10)
    print(ticket)
