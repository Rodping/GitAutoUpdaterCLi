import json
import os
import time

# Základní proměnné projektu
ORIGIN_DIR = ""
TEMP_DIR = ""
CONTENT_DIR = ""
SCRIPTS_DIR = ""
REPO_URL = ""
REPO_DIR = ""
TEMP_FILE_NAME = "temp_variables.json"
TEMP_FILE = ""


class TempVariables:
    """Jednoduchá třída pro uložení a načtení proměnných projektu na disk."""
    
    def __init__(self, origin_dir=None, repo_dir=None, file_name="temp_variables.json"):
        self.ORIGIN_DIR = self._detect_origin_dir()
        self.REPO_URL = ""
        self._storage_file_name = file_name
        self._storage_file = None
        self._setup_directories()
        # 1. Спочатку загрузити старші дані з диску
        self.load_from_disk()
        # 2. Аж ТЕПЕР використовувати параметри із сучасного бізу і з тим переписати старі дані
        if origin_dir:
            self.ORIGIN_DIR = origin_dir
        if repo_dir:
            self.REPO_DIR = repo_dir
        elif not hasattr(self, 'REPO_DIR'):
            self.REPO_DIR = self.ORIGIN_DIR
        # 3. Зберешти відразу новий і правильний стан
        self.save_to_disk()

    def _detect_origin_dir(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def _setup_directories(self):
        path = os.path
        self.TEMP_DIR = path.join(self.ORIGIN_DIR, "temp")
        self.CONTENT_DIR = path.join(self.ORIGIN_DIR, "content")
        self.SCRIPTS_DIR = path.join(self.ORIGIN_DIR, "python_scripts")
        os.makedirs(self.TEMP_DIR, exist_ok=True)
        self._storage_file = path.join(self.TEMP_DIR, self._storage_file_name)

    def _resolve_storage_file(self):
        if not self._storage_file:
            self._storage_file = os.path.join(self.TEMP_DIR, self._storage_file_name)
        return self._storage_file

    def remove_storage_file(self):
        file_path = self._resolve_storage_file()
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except OSError as exc:
            print(f"Chyba při mazání souboru {file_path}: {exc}")
        return file_path

    def save_to_disk(self):
        payload = {}
        for key in ("ORIGIN_DIR", "TEMP_DIR", "CONTENT_DIR", "SCRIPTS_DIR", "REPO_URL", "REPO_DIR"):
            if hasattr(self, key):
                payload[key] = getattr(self, key)

        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            if key in payload:
                continue
            payload[key] = value

        file_path = self._resolve_storage_file()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.remove_storage_file()
        with open(file_path, "w", encoding="utf-8") as soubor:
            json.dump(payload, soubor, ensure_ascii=False, indent=4)
        return file_path

    def load_from_disk(self):
        file_path = self._resolve_storage_file()
        if not os.path.isfile(file_path):
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as soubor:
                payload = json.load(soubor)
        except (json.JSONDecodeError, OSError) as exc:
            print(f"Chyba při načítání souboru {file_path}: {exc}")
            return None

        for key, value in payload.items():
            if key.startswith("_"):
                continue
            object.__setattr__(self, key, value)
        return file_path

    def set_value(self, name, value):
        object.__setattr__(self, name, value)
        self.save_to_disk()
        return value

    def delete_value(self, name):
        if hasattr(self, name):
            object.__delattr__(self, name)
            self.save_to_disk()
            return True
        return False

    def get_value(self, name, default=None):
        if not hasattr(self, name):
            self.load_from_disk()
        return getattr(self, name, default)

    def get_all_directories(self):
        return {
            "ORIGIN_DIR": self.ORIGIN_DIR,
            "TEMP_DIR": self.TEMP_DIR,
            "CONTENT_DIR": self.CONTENT_DIR,
            "SCRIPTS_DIR": self.SCRIPTS_DIR,
            "REPO_URL": self.REPO_URL,
            "REPO_DIR": self.REPO_DIR,
        }

    def __str__(self):
        dirs = self.get_all_directories()
        output = "TempVariables:\n"
        for key, value in dirs.items():
            output += f"  {key}: {value}\n"
        return output


_SHARED_TEMP_VARIABLES = None


def initialize_temp_variables(origin_dir=None, repo_dir=None, file_name="temp_variables.json", force_new=False):
    global _SHARED_TEMP_VARIABLES
    if _SHARED_TEMP_VARIABLES is None or force_new:
        _SHARED_TEMP_VARIABLES = TempVariables(origin_dir=origin_dir, repo_dir=repo_dir, file_name=file_name)
        return _SHARED_TEMP_VARIABLES

    if origin_dir is not None:
        _SHARED_TEMP_VARIABLES.ORIGIN_DIR = origin_dir
    if repo_dir is not None:
        _SHARED_TEMP_VARIABLES.REPO_DIR = repo_dir

    _SHARED_TEMP_VARIABLES._setup_directories()
    _SHARED_TEMP_VARIABLES.save_to_disk()
    return _SHARED_TEMP_VARIABLES


def get_temp_variables(origin_dir=None, repo_dir=None, file_name="temp_variables.json"):
    return initialize_temp_variables(origin_dir=origin_dir, repo_dir=repo_dir, file_name=file_name)


def set_temp_value(name, value):
    return get_temp_variables().set_value(name, value)


def get_temp_value(name, default=None):
    return get_temp_variables().get_value(name, default)


if __name__ == "__main__":
    tv = TempVariables()
    tv.set_value("demo_value", "hello")
    print(tv.get_value("demo_value"))
    print(tv.get_all_directories())
