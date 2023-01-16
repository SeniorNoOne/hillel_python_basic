from classes.notebook import Notebook
from src.notebook.classes.custom_exceptions import CSVHandlerError
from utils.config import CSV_FILE_DIR, CONFIGS, INP_OPTIONS, ROWS_SPACER


if __name__ == "__main__":
    with Notebook(CSV_FILE_DIR, CONFIGS, INP_OPTIONS, ROWS_SPACER) as notebook:
        notebook.show_notebook()
        while True:
            try:
                notebook.ui.show_interface()
                user_inp = notebook.ui.get_user_inp("Enter what you "
                                                    "want to do: ")
                if user_inp in INP_OPTIONS:
                    notebook.run_func(user_inp)
                else:
                    notebook.ui.display("There is no such option. Try again")
            except CSVHandlerError:
                pass
