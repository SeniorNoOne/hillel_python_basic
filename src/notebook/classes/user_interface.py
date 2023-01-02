from src.notebook.utils.config import INP_OPTIONS, ROWS_SPACER


class UserInterface:
    def __init__(self, interface_options: dict, row_spacer: str = ""):
        self.interface_options = interface_options
        self.row_spacer = row_spacer

    def show_interface(self):
        print(self.row_spacer)
        print("Choose what you want to do:")
        for index, option in self.interface_options.items():
            self.display(f"{index} - {option['name']}")
        print(self.row_spacer)

    @staticmethod
    def get_user_inp(message: str = "") -> str:
        return input(message).strip()

    @staticmethod
    def display(message: str) -> None:
        print(message)


if __name__ == "__main__":
    interface = UserInterface(INP_OPTIONS, ROWS_SPACER)
    interface.show_interface()
