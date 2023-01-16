import csv
import os.path
from src.notebook.classes.custom_exceptions import CSVHandlerError


class CSVHandler:
    def __call__(self, file_dir: str, headers: list, mode: str = "r"):
        return self._get_creator(file_dir, headers, mode)

    @staticmethod
    def _get_creator(file_dir: str, headers: list, mode: str):
        match mode:
            case "r":
                return CSVReader(file_dir, headers)
            case "w":
                return CSVWriter(file_dir, headers)
            case "wr" | "rw":
                return CSVReaderWriter(file_dir, headers)
            case _:
                raise ValueError(f"Invalid mode - {mode}")


class CSVReader:
    def __init__(self, file_dir: str, headers: list):
        if os.path.isfile(file_dir):
            self.csv_file_dir = file_dir
            self.csv_headers = headers
            self.read_file = open(self.csv_file_dir, "r", newline="")
            self.csv_reader = csv.DictReader(self.read_file,
                                             fieldnames=self.csv_headers)
            self.csv_data = list(self.csv_reader)
        else:
            raise CSVHandlerError(f"Wrong file name or path - {file_dir}")

    def __iter__(self):
        return iter(self.csv_data)

    def close(self):
        print(f"Closing file - {self}")
        self.read_file.close()


class CSVWriter:
    def __init__(self, file_dir: str, headers: list):
        if os.path.isfile(file_dir):
            self.csv_file_dir = file_dir
            self.csv_headers = headers
            self.write_file = open(self.csv_file_dir, "w", newline="")
            self.csv_writer = csv.DictWriter(self.write_file,
                                             fieldnames=self.csv_headers,
                                             quoting=csv.QUOTE_NONNUMERIC)
        else:
            raise CSVHandlerError(f"Wrong file name or path - {file_dir}")

    def write_row(self, row: dict):
        self.csv_writer.writerow(row)

    def write_rows(self, rows: list):
        self.csv_writer.writerows(rows)

    def close(self):
        print(f"Closing file - {self}")
        self.write_file.close()


class CSVReaderWriter(CSVReader, CSVWriter):
    def __init__(self, file_dir: str, headers: list):
        if os.path.isfile(file_dir):
            CSVReader.__init__(self, file_dir, headers)
            CSVWriter.__init__(self, file_dir, headers)
        else:
            raise CSVHandlerError(f"Wrong file name or path - {file_dir}")

    def close(self):
        print(f"Closing file - {self}")
        self.read_file.close()
        self.write_file.close()


if __name__ == "__main__":
    handler = CSVHandler()
    handler("some_file_dir", [], "p")
