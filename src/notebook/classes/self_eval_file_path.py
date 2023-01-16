import os


class SelfEvalFilePath:
    def __init__(self, filepath: str = ""):
        self._filepath = filepath

    @property
    def filepath(self):
        current_path = os.getcwd().split(os.sep)
        new_path = []
        for item in current_path:
            if item not in self._filepath:
                new_path.append(item)
            else:
                break
        current_path = f"{os.sep}".join(new_path) + os.sep
        return self._filepath.replace(f".{os.sep}", current_path)
