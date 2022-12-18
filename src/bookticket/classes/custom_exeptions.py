class TicketError(Exception):
    pass


if __name__ == "__main__":
    raise TicketError("Test error")
