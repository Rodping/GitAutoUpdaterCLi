import os
import subprocess
import time
import threading
from colorama import Fore, Back, Style
import git
try:
    import python_scripts.checker as checker
    import python_scripts.variables as variables
except Exception as e:
    print(f"Загрузка компонентів не пішла, помилка: {e}")
    import checker
    import variables
# --- NASTAVENÍ ---
# SSH URL (doporučeno) nebo HTTPS URL s tokenem
REPO_URL = "https://github.com/Rodping/PLastHub.git"
ORIGIN_DIR = ""
TEMP_DIR = ""
CONTENT_DIR = ""
SCRIPTS_DIR = ""
REPO_DIR = ""

isrunning = False

TempVars= None

input_received = False
cycle_count = 0
actual_branch = ""

# Interval v sekundách (5 minut = 300 sekund)

########## func ###########
def color_text_fore(text: str, color: str):
    color_code = getattr(Fore, color.upper(), Fore.WHITE)
    return(color_code + text + Style.RESET_ALL)

def update_repo(TARGET_DIR, selected_branch):
    if not TARGET_DIR:
        raise ValueError("REPO_DIR не встановлено. Переконайся, що setup_directories() викликано перед start().")
    
    Aktualni_cas = time.strftime("%Y-%m-%d %H:%M:%S")
    print(color_text_fore(f"[{Aktualni_cas}] Синхронізація...", "green"))

    TEMP_DIR = os.path.abspath(os.path.join(os.path.dirname(TARGET_DIR), "temp"))

    #repo.git.checkout(selected_branch)
    try:
        # Kontrola, zda už existuje složka .git
        if os.path.exists(os.path.join(TARGET_DIR, ".git")):
            print("Репо знайдено, оновлюю...")
            # Spustí 'git pull' přímo v cílovém adresáři
            subprocess.run(["git", "pull"], cwd=TARGET_DIR, check=True)

        else:
            print("Ненайшов репо, клоную...")
            os.makedirs(TARGET_DIR, exist_ok=True)
            subprocess.run(["git", "clone", REPO_URL, TARGET_DIR], check=True)

        print("-> Готово. Всі файли оновлені.")

        # repo = git.Repo(TARGET_DIR)
        # repo.git.checkout(selected_branch)
        # repo.git.pull()
        print(f"-> Обрав '{selected_branch}' вітку для використання.\n")

    except subprocess.CalledProcessError as e:
        print(f"-> ПОМИЛКА: Команда Gitu не вдалася: {e}\n")
    except Exception as e:
        print(f"-> НЕОЧІКУВАНА ПОМИЛКА: {e}\n")

    # checker.python_file_check(ORIGIN_DIR, TEMP_DIR)
    



def start(branch, interval=300):
    # import variables
    global ORIGIN_DIR, isrunning, REPO_DIR, actual_branch, cycle_count

    INTERVAL = interval
    actual_branch = branch
    TempVars = variables.get_temp_variables(origin_dir=ORIGIN_DIR or None, repo_dir=REPO_DIR or None)

    if INTERVAL % 60 == 0:
        interval_text = f"{INTERVAL // 60} minut"
    else:
        interval_text = f"{INTERVAL} sekund"
    print(f"AutoUpdate запушчен. Провірка буде кождних {interval_text}.")
    print("Про вихід нажми Ctrl+C.\n")

    isrunning = True
    actual_cycle_count = cycle_count
    try:
        while True:
            if isrunning:
                if cycle_count > actual_cycle_count:
                    break  # Pokud se počet cyklů změnil, ukončíme smyčku
                update_repo(REPO_DIR, branch)
                time.sleep(INTERVAL)
            else:
                time.sleep(1)  # Krátká pauza, aby smyčka zbytečně nezatěžovala procesor
            
    except KeyboardInterrupt:
        print("\nLEFT THE SCRIPT by user.")

def stop():
    global isrunning, cycle_count
    isrunning = False
    cycle_count = cycle_count + 1
    print("AutoUpdate script STOPPED.")

def resume(branch, interval=300):
    global isrunning, actual_branch
    _interval = 200
    if not isrunning:
        if branch:
            actual_branch = branch
        if interval and interval != 300:
            _interval = interval
        isrunning = True
        start(actual_branch, interval=_interval)
        print("AutoUpdate script RESUMED.")
    else:
        print("AutoUpdate script is already running.")


def get_directories():
    global ORIGIN_DIR, TEMP_DIR, TEMP_FILE, TEMP_FILE_NAME, CONTENT_DIR, SCRIPTS_DIR, REPO_DIR, Directories
    Directories = variables.get_temp_variables(origin_dir=ORIGIN_DIR or None, repo_dir=REPO_DIR or None)  # type: ignore
    ORIGIN_DIR = Directories.ORIGIN_DIR
    TEMP_DIR = Directories.TEMP_DIR
    CONTENT_DIR = Directories.CONTENT_DIR
    SCRIPTS_DIR = Directories.SCRIPTS_DIR
    REPO_DIR = Directories.REPO_DIR
    variables.set_temp_value("REPO_URL", REPO_URL)
    print(variables.get_temp_variables())
if __name__ == "__main__":
    print("Запускайте StartServer.py, а не auto_git_update_5min.py")
    exit(1)