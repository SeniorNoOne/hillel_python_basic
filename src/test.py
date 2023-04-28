import src.bookticket.config as config
import csv

import os.path
from random import choice, randint
from src.bookticket.classes.bus import Bus


class CSVHandlerError(Exception):
    pass


class CSVHandler:
    def __call__(self, file_dir, mode="r"):
        return self._get_creator(file_dir, mode)

    @staticmethod
    def _get_creator(file_dir, mode):
        match mode:
            case "r":
                return CSVReader(file_dir)
            case "w":
                return CSVWriter(file_dir)
            case "wr" | "rw":
                return CSVReaderWriter(file_dir)
            case _:
                raise CSVHandlerError("Wrong mode")


class CSVReader:
    def __init__(self, file_dir, headers):
        if os.path.isfile(file_dir):
            self.csv_file_dir = file_dir
            self.headers = headers
            self.read_file = open(self.csv_file_dir, "r", newline="")
            self.csv_reader = csv.DictReader(self.read_file,
                                             fieldnames=self.headers)
            self.csv_data = list(self.csv_reader)
        else:
            raise CSVHandlerError("Wrong format")

    def read_row(self):
        return iter(self.csv_data)

    def read_rows(self):
        return self.csv_data

    def __iter__(self):
        return iter(self.csv_data)

    def close(self):
        print("Closing read file")
        self.read_file.close()


class CSVWriter:
    def __init__(self, file_dir, headers):
        if os.path.isfile(file_dir):
            self.csv_file_dir = file_dir
            self.headers = headers
            self.write_file = open(self.csv_file_dir, "a", newline="")
            self.csv_writer = csv.DictWriter(self.write_file,
                                             fieldnames=self.headers,
                                             quoting=csv.QUOTE_NONNUMERIC)
        else:
            raise CSVHandlerError("Wrong format")

    def write_row(self, row):
        self.csv_writer.writerow(row)

    def write_rows(self, rows):
        self.csv_writer.writerows(rows)

    def close(self):
        print("Closing write file")
        self.write_file.close()


class CSVReaderWriter(CSVReader, CSVWriter):
    def __init__(self, file_dir):
        if os.path.isfile(file_dir):
            CSVReader.__init__(self, file_dir)
            CSVWriter.__init__(self, file_dir)
        else:
            pass

    def close(self):
        print("Closing files")
        self.read_file.close()
        self.write_file.close()

    def update_reader(self, func):
        def wrapper(*args):
            func(*args)
            self.csv_reader = csv.reader(self.read_file)
            self.csv_data = list(self.csv_data)
        return wrapper


routes = [
    ("2022-12-22, 08:00", "Zhashkiv-Odesa"),
    ("2022-12-22, 10:00", "Zhashkiv-Odesa"),
    ("2022-12-22, 12:00", "Zhashkiv-Odesa"),
    ("2022-12-10, 14:00", "Zhashkiv-Odesa"),
    ("2022-12-23, 16:00", "Zhashkiv-Kyiv"),
    ("2022-12-23, 18:00", "Zhashkiv-Kyiv"),
    ("2022-12-23, 20:00", "Zhashkiv-Kyiv"),
    ("2022-12-10, 22:00", "Zhashkiv-Kyiv"),
    ("2022-12-25, 08:00", "Zhashkiv-Poltava"),
    ("2022-12-25, 10:00", "Zhashkiv-Poltava"),
    ("2022-12-25, 12:00", "Zhashkiv-Poltava"),
    ("2022-12-25, 14:00", "Zhashkiv-Poltava"),
    ("2022-12-11, 16:00", "Zhashkiv-Poltava"),
    ("2022-12-26, 06:00", "Zhashkiv-Lviv"),
    ("2022-12-26, 10:00", "Zhashkiv-Lviv"),
    ("2022-12-26, 16:00", "Zhashkiv-Lviv"),
    ("2022-12-11, 20:00", "Zhashkiv-Lviv"),
    ("2022-12-27, 8:00", "Zhashkiv-Uman"),
    ("2022-12-27, 10:00", "Zhashkiv-Uman"),
    ("2022-12-12, 12:00", "Zhashkiv-Uman")
]

buses = [
    (0,39,"KT7209ES"),
    (1,32,"EL8452UG"),
    (2,30,"FZ4151HG"),
    (3,26,"ET5903MJ"),
    (4,34,"OO5291DZ"),
    (5,32,"HB1121SS"),
    (6,25,"YQ2182UH"),
    (7,40,"XS1961MV"),
    (8,37,"CG8484WR"),
    (9,31,"YC6359CR"),
    (10,29,"EO9930YF"),
    (11,36,"WM9915KR"),
    (12,26,"HM2633PF"),
    (13,39,"LH4743LL"),
    (14,34,"GS4811PR")]


if __name__ == "__main__":
    csv_factory = CSVHandler()
    file = csv_factory(config.files_dir_test["buses"], "wr")
    headers = config.csv_headers["buses"]

    while True:
        input_option = input("1 - read, 2 - write: ")
        match input_option:
            case "1":
                for line in file:
                    print(line)
            case "2":
                for index, bus in enumerate(buses):
                    bus = {headers[i]: bus[i] for i in range(3)}
                    file.write_row(bus)
            case _:
                print("Wrong")
                exit(0)
