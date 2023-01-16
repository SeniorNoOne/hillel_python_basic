import re


class SeqUtils:
    @staticmethod
    def get_list_of_ints_from_str(string):
        string = [item for item in string.replace(" ", "").split(",") if item]
        string = [*dict.fromkeys(string)]
        if all([item for item in string if item.isdigit()]):
            return [int(item) for item in string]
        else:
            return []

    @staticmethod
    def regex_from_str(re_str):
        re_str = re_str.strip()
        re_str = re_str.replace("*", ".*")
        return re.compile(re_str, re.IGNORECASE)


if __name__ == "__main__":
    utils = SeqUtils()
