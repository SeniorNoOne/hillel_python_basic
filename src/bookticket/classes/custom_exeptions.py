class TicketError(Exception):
    pass


class CSVHandlerError(Exception):
    pass


if __name__ == "__main__":
    # raise TicketError("Test error")
    raise CSVHandlerError("some_wrong_dir")
