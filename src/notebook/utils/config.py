import re
from src.notebook.classes.self_eval_file_path import SelfEvalFilePath

INP_OPTIONS = {
    "1":
        {
            "name": "Create new record",
            "func": "add_record",
            "func_arg": None
        },

    "2":
        {
            "name": "Delete existing record",
            "func": "delete_records",
            "func_arg": None
        },

    "3":
        {
            "name": "Edit existing record",
            "func": "edit_record",
            "func_arg": None
        },

    "4":
        {
            "name": "Search record by user first name",
            "func": "search_records",
            "func_arg": "first_name"
        },

    "5":
        {
            "name": "Search record by user last name",
            "func": "search_records",
            "func_arg": "last_name"
        },

    "6":
        {
            "name": "Search record by phone number",
            "func": "search_records",
            "func_arg": "phone_number"
        },

    "7":
        {
            "name": "Sort records by user first name",
            "func": "sort_records",
            "func_arg": "first_name"
        },

    "8":
        {
            "name": "Sort records by user last name",
            "func": "sort_records",
            "func_arg": "last_name"
        },

    "9":
        {
            "name": "Show records",
            "func": "show_records",
            "func_arg": None
        },

    "0":
        {
            "name": "Exit",
            "func": "close_notebook",
            "func_arg": None
        }
}

CONFIGS = {
    "id": {
        "type": int,
        "default_val": None,
        "add_record_required": False,
        "add_record_skippable": True,
        "add_record_func": "add_id",
        "output_str": "ID",
        "error_msg": "ID must be a number. IDs must be separated by comma "
                     "if multiple are provided",
        "re": re.compile(r"^(\d+)$"),
        "re_join_sep": "",
    },

    "first_name": {
        "type": str,
        "default_val": "-",
        "add_record_required": True,
        "add_record_skippable": False,
        "add_record_func": "",
        "output_str": "first name",
        "error_msg": "First name must consist of only alphabetic characters "
                     "and be longer than 3 characters",
        "re": re.compile(r"^((?:[A-Z][a-z]{2,})|quit)$"),
        "re_join_sep": "",
    },

    "last_name": {
        "type": str,
        "default_val": "-",
        "add_record_required": True,
        "add_record_skippable": False,
        "add_record_func": "",
        "output_str": "last name",
        "error_msg": "Last name must consist of only alphabetic characters and "
                     "be longer than 3 characters ",
        "re": re.compile(r"^((?:[A-Z][a-z]{2,})|quit)$"),
        "re_join_sep": "",
    },

    "phone_number": {
        "type": str,
        "default_val": "-",
        "add_record_required": True,
        "add_record_skippable": False,
        "add_record_func": "add_default_val",
        "output_str": "phone number",
        "error_msg": "Phone number must have the following format - "
                     "XXX XX XXX XX XX",
        "re": re.compile(r"^[+]?[(]?(\d{3})[)]?[-\s.]?(\d{2})[-\s.]?(\d{3})"
                         r"[-\s.]?(\d{2})[-\s.]?(\d{2}).{0}|(quit)$"),
        "re_join_sep": "-",
    },

    "address": {
        "type": str,
        "default_val": "-",
        "add_record_required": True,
        "add_record_skippable": True,
        "add_record_func": "add_default_val",
        "output_str": "address",
        "error_msg": "Address must have the following format - City name, "
                     "Street, House number, Flat number (optional)",
        "re": re.compile(r"^([\w ]+)[, ]+([\w .]+)[, ]+(\d*)[, ]+([\w ]*)|"
                         r"(quit)$"),
        "re_join_sep": ", ",
    },

    "birthdate": {
        "type": str,
        "default_val": "-",
        "add_record_required": True,
        "add_record_skippable": True,
        "add_record_func": "add_default_val",
        "output_str": "birth date",
        "error_msg": "Date of birth must have the following format - "
                     "Day Month Year",
        "re": re.compile(r"^([1-2][0-9]|3[0-1])[-. ](0[1-9]|1[0-2])[-. ]"
                         r"(19[0-9][0-9]|20[0-1][0-9]|202[0-3])|(quit)$"),
        "re_join_sep": ".",
    }
}

# CSV file dir relative to src folder. Used in determining of absolute path
_CSV_FILE_PATH = r".\notebook\utils\records.csv"
CSV_FILE_DIR = SelfEvalFilePath(_CSV_FILE_PATH).filepath
ROWS_SPACER = "-" * 100


if __name__ == "__main__":
    print(CSV_FILE_DIR)
