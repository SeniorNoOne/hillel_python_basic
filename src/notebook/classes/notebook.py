import os.path
import re
from tabulate import tabulate
from src.notebook.classes.csv_handler import CSVHandler
from src.notebook.classes.helpers import SeqUtils
from src.notebook.classes.user_interface import UserInterface
from src.notebook.utils.config import CSV_FILE_DIR, CONFIGS
from src.notebook.utils.config import INP_OPTIONS, ROWS_SPACER


class Notebook:
    def __init__(self, file_path, configs, interface_configs, ui_spacer):
        self.file_path = file_path
        self.configs = configs
        self.records = []
        self.used_id = []
        self.re_match = None
        self.user_inp = ""

        # helping functions
        self.utils = SeqUtils()

        # opening CSV file
        self.csv_handler = CSVHandler()
        self.csv_file = self.csv_handler(self.file_path,
                                         list(self.configs.keys()), "wr")

        # setting flag and numbers of rows if CSV file exists
        self.is_file_exist = os.path.exists(self.file_path)
        self.file_is_opened = True
        self.records_num = len(list(self.csv_file))
        self.records = self.convert_records_type(self.csv_file.csv_data)
        self.used_id = [record["id"] for record in self.records]

        # creating user interface
        self.ui = UserInterface(interface_configs, ui_spacer)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_notebook()

    def __del__(self):
        self.close_notebook()

    def show_notebook(self):
        if self.records_num:
            self.ui.display(f"Loaded {self.records_num} records from file")

    def show_record(self, record: dict) -> None:
        if record:
            headers = [self.configs[field]["output_str"].capitalize() for
                       field in self.configs]
            table = tabulate([record.values()], headers=headers,
                             tablefmt="simple_outline")
            self.ui.display(table)
        else:
            self.ui.display("Record is empty. Nothing to show")

    def show_records(self, records: list = ()) -> None:
        # if records parameter is not provided we'll try to show self.records
        if not records:
            records = self.records
        # showing records if list is not empty
        if records:
            headers = [self.configs[item]["output_str"].capitalize() for
                       item in self.configs]
            data_to_show = {field: [value[field] for value in records] for field
                            in self.configs}
            table = tabulate(data_to_show, headers=headers,
                             tablefmt="simple_outline")
            self.ui.display(table)
        else:
            self.ui.display("Records are empty. Nothing to show")

    def inp_show_records(self, message: str) -> bool:
        inp = self.ui.get_user_inp(f"{message} (y - yes): ")
        inp = inp.strip().lower() == "y"
        return inp

    def convert_records_type(self, records: list) -> list:
        for record in records:
            for field in record:
                record[field] = self.configs[field]["type"](record[field])
        return records

    def convert_input_type(self, inp: list, field: str) -> list:
        field_type = self.configs[field]["type"]
        if field_type is not str:
            for index, item in enumerate(inp):
                inp[index] = field_type(item)
        return inp

    def validate_user_input(self, field: str) -> bool:
        regex = self.configs[field]["re"]
        self.re_match = re.fullmatch(regex, self.user_inp)
        is_re_matched = bool(self.re_match)
        # True if object matched regex or when user provided empty input and
        # record field can be skipped
        return is_re_matched or (self.configs[field]["add_record_skippable"]
                                 and not self.user_inp)

    def process_re_match(self, field: str) -> list:
        re_sep = self.configs[field]["re_join_sep"]
        # join match results if regex matched
        if self.re_match:
            match_res = re_sep.join([item for item in
                                     self.re_match.groups(default="") if item])
        # otherwise initialize field with its default value
        else:
            match_res = self.configs[field]["default_val"]
        return match_res

    def process_user_input(self, field: str, edit_record_mode=False):
        # Flag 'edit_record_mode' defines behaviour of method
        # True corresponds to call from 'edit_record' method
        # False  corresponds to call from 'add_records' method
        is_invalid_inp = True
        put_asterisk = not self.configs[field]['add_record_skippable']
        output_str = f"Enter your {self.configs[field]['output_str']}" \
                     f"{'*' * put_asterisk}: "
        while is_invalid_inp:
            self.user_inp = self.ui.get_user_inp(output_str)
            is_invalid_inp = not self.validate_user_input(field)
            if edit_record_mode:
                # empty input is valid input when method called
                # from 'edit_record' method
                is_invalid_inp = self.user_inp and is_invalid_inp
            if is_invalid_inp:
                self.ui.display(self.configs[field]["error_msg"])
        return self.process_re_match(field)

    def add_id(self) -> int:
        return self.records_num

    def create_new_record(self, edit_record_mode=False) -> dict | None:
        new_record = {field: None for field in self.configs}
        self.ui.display("Fields with '*' are mandatory to fill. "
                        "Enter 'quit' to stop entering new record")
        for field in self.configs:
            if self.configs[field]["add_record_required"]:
                record_field = self.process_user_input(field, edit_record_mode)
                if record_field == "quit":
                    return None
            else:
                # if field is not required (like ID) its value obtained by
                # calling special method
                record_field = getattr(self, self.configs[field][
                    "add_record_func"])()
            new_record[field] = record_field
        return new_record

    def add_record(self) -> None:
        new_record = self.create_new_record()
        if new_record:
            self.records_num += 1
            self.records.append(new_record)
            self.ui.display("New record has been successfully created")
        else:
            self.ui.display("Quitting")

    def process_ids_to_remove(self, ids_to_remove: list) -> None:
        records = []
        removed_records = []
        for record in self.records:
            if record["id"] in ids_to_remove:
                removed_records.append(record)
            else:
                records.append(record)
        self.records_num -= len(ids_to_remove)
        self.records = records
        self.ui.display(f"Records with specified ID's were removed")
        self.show_records(removed_records)

    def delete_records(self) -> None:
        if self.records:
            if self.inp_show_records("Show records"):
                self.show_records()
            output_str = f"Enter record ID's that you want to remove: "
            ids_to_remove = self.ui.get_user_inp(output_str)
            if ids_to_remove != "quit":
                ids_to_remove = self.utils.get_list_of_ints_from_str(
                    ids_to_remove)
                if ids_to_remove and \
                        all([_id in self.used_id for _id in ids_to_remove]):
                    self.process_ids_to_remove(ids_to_remove)
                else:
                    self.ui.display("Specified ID doesn't exist or "
                                    "ID format is wrong")
                    self.ui.display(self.configs["id"]["error_msg"])
            else:
                self.ui.display("Quitting")
        else:
            self.ui.display("There are no records in notebook")

    def search_records_by_mask(self, field: str, mask) -> list:
        value_to_find = self.utils.regex_from_str(mask)
        found_records = [record for record in self.records if
                         re.fullmatch(value_to_find, record[field])]
        return found_records

    def search_records_by_field_val(self, field: str, value) -> list:
        if isinstance(value, str):
            found_records = [record for record in self.records if
                             record[field].lower() == value.lower()]
        else:
            found_records = [record for record in self.records if
                             record[field] == value]
        return found_records

    def search_records(self, field: str) -> None:
        if self.inp_show_records("Show records"):
            self.show_records()
        output_str = self.configs[field]["output_str"]
        regex = re.compile(self.configs[field]["re"].pattern, re.IGNORECASE)
        re_sep = self.configs[field]["re_join_sep"]
        value_to_find = self.ui.get_user_inp(f"Enter {output_str} you "
                                             f"searching for: ")
        found_records = None

        if "*" in value_to_find:
            found_records = self.search_records_by_mask(field, value_to_find)
        else:
            if value_to_find := re.fullmatch(regex, value_to_find):
                value_to_find = [item for item in
                                 value_to_find.groups() if item]
                value_to_find = re_sep.join(value_to_find)
                found_records = self.search_records_by_field_val(
                    field, value_to_find)
            else:
                self.ui.display(self.configs[field]["error_msg"])

        if found_records:
            self.show_records(found_records)
        else:
            self.ui.display(f"No records have been found")

    def sort_records_by_field(self, field: str, is_reversed=False) -> list:
        return sorted(self.records, key=lambda record: record[field],
                      reverse=is_reversed)

    def sort_records(self, field) -> None:
        is_reversed = self.inp_show_records("Sort in descending order")
        if self.records:
            sorted_records = self.sort_records_by_field(field, is_reversed)
            self.show_records(sorted_records)
        else:
            self.ui.display("So far nothing to sort")

    def process_edited_record(self, record: dict) -> None:
        if new_record := self.create_new_record(edit_record_mode=True):
            for field in record:
                if field == "id":
                    continue
                if new_record[field] != self.configs[field]["default_val"]:
                    record[field] = new_record[field]
            self.ui.display(f"Record with ID {record['id']} has "
                            f"been successfully changed")
            self.show_record(record)
        else:
            self.ui.display("Quitting")

    def edit_record(self) -> None:
        output_str = f"Enter record {self.configs['id']['output_str']} " \
                     f"that you want to edit: "
        if self.inp_show_records("Show records"):
            self.show_records()

        id_to_edit = self.ui.get_user_inp(output_str)
        if id_to_edit != "quit":
            if id_to_edit and id_to_edit.isdigit():
                id_to_edit = self.configs["id"]["type"](id_to_edit)
                if id_to_edit in self.used_id:
                    record_to_edit = self.search_records_by_field_val(
                        "id", id_to_edit)[-1]
                    self.process_edited_record(record_to_edit)
                else:
                    self.ui.display("There is no record with such ID")
            else:
                self.ui.display(self.configs["id"]["error_msg"].split(".")[0])
        else:
            self.ui.display("Quitting")

    def close_notebook(self):
        # this block of code must be executed only once
        if self.file_is_opened:
            self.ui.display("Writing all records in file and closing notebook")
            self.csv_file.write_rows(self.records)
            self.csv_file.close()
            self.file_is_opened = False
            exit()

    def run_func(self, option: str) -> None:
        func_arg = self.ui.interface_options[option]["func_arg"]
        func = self.ui.interface_options[option]["func"]
        if func_arg:
            getattr(self, func)(func_arg)
        else:
            getattr(self, func)()


if __name__ == "__main__":
    notebook = Notebook(CSV_FILE_DIR, CONFIGS, INP_OPTIONS, ROWS_SPACER)
