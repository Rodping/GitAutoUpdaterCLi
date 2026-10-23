import os
import subprocess
from python_scripts import auto_git_update_5min as auto_git_update
from python_scripts import variables 
from python_scripts.variables import TempVariables
from python_scripts import ConsoleDebug
import colorama
from colorama import Fore, Back, Style
import threading
import time
import git
# import sys
# from readkeys import getkey 
# import keyboard # Тільки для компютерів
"""

StarterServer.py заавжди мусить бути в папці /PlastHub/, 
бо інакше, весь все ламаєтся

Назви папок:
----------------------------------------
origin_dir, temp_dir, content_dir, scripts_dir, repo_dir
global ORIGIN_DIR, TEMP_DIR, TEMP_FILE, TEMP_FILE_NAME, CONTENT_DIR, SCRIPTS_DIR, REPO_DIR, Directories
ORIGIN_DIR = 
TEMP_DIR = 
CONTENT_DIR = 
SCRIPTS_DIR = 
REPO_DIR = 


Directories.ORIGIN_DIR = ORIGIN_DIR
Directories.TEMP_DIR = TEMP_DIR
Directories.TEMP_FILE = TEMP_FILE
Directories.CONTENT_DIR = CONTENT_DIR
Directories.SCRIPTS_DIR = SCRIPTS_DIR
Directories.REPO_DIR = REPO_DIR


"""
########## func ###########
def color_text_fore(text: str, color: str):
    color_code = getattr(Fore, color.upper(), Fore.WHITE)
    return(color_code + text + Style.RESET_ALL)

path = os.path

# def wait_for_input
input_received = False
waiting_for_input = False
input_text = ""
input_text_final = ""
###########################

ORIGIN_DIR = path.dirname(__file__) # - Самотній сервер, або папка сервера
REPO_DIR = ""
SCRIPTS_DIR = path.join(ORIGIN_DIR, "python-scripts")

print(color_text_fore("Папка серверу: ", "green") + ORIGIN_DIR)
vybrana_vetev = ""

def wait_for_input(question, timeout: int = 10):
    global waiting_for_input, input_received, input_text
    input_received = False
    input_text = ""

    thread_parent = threading.Thread(target=wait_for_input_deamon, args=(question,))
    thread_parent.daemon = True
    thread_parent.start()

    waiting_for_input = True
    start_time = time.time()
    while time.time() - start_time < timeout:
        if input_received:
            break
        time.sleep(0.1) # Krátká pauza, aby smyčka zbytečně nezatěžovala procesor
    waiting_for_input = False
    return input_text


def wait_for_input_deamon(question):
    global input_received, waiting_for_input, input_text
    try:
        input_text = input(question)
        input_received = True
        if waiting_for_input:
            waiting_for_input = False
        else:
            input_text = ""
    except EOFError:
        pass

def get_parent_directory():
    global ORIGIN_DIR, REPO_DIR, waiting_for_input

    # 1. Вибери папку для збереження

    text_for_dir_quest = (r"Задай дорогу к папці (нічого не напишеш, тоді збереження о '..\repo\' )"+
                           "\n------> ")
    REPO_DIR = wait_for_input(text_for_dir_quest, timeout = 10)
    
    
    if(REPO_DIR == "test" or os.path.isfile(os.path.join(ORIGIN_DIR, "TEST"))):
        
        repo = path.join(ORIGIN_DIR, "repo")
        os.makedirs(repo, exist_ok=True)
        REPO_DIR = repo
    elif(not REPO_DIR):
        # ORIGIN_DIR = os.path.dirname(__file__) --- PlastHub/
        print(color_text_fore("Не можу розпізнати папку, використовою папку сайта!!!", "red"))
        REPO_DIR = path.join(ORIGIN_DIR)
    print(color_text_fore("\nВикористовую папку: ", "green") + REPO_DIR)

def select_branch():
    global REPO_DIR, vybrana_vetev
    # 2. Вибери вітку для копіюівння
    try:
        # 0. Перевірка чи це є дійсний репо
        if not os.path.exists(os.path.join(REPO_DIR, ".git")):
            ConsoleDebug.message("Порожня папка: Репозиторіц не існує. Я пропускаю вибір гілок і дозволяю репозиторію завантажуватися.")
            vybrana_vetev = ""
            return
        # --- Фікс безпечної безпеки Гіту на Андройд  ---
        subprocess.run(["git", "config", "--global", "--add", "safe.directory", REPO_DIR], check=False)
        # -----------------------------------------------

        # 1. Otevření existujícího repozitáře (zadejte cestu k vašemu projektu)
        repo = git.Repo(REPO_DIR)

        # 2. Výpis všech lokálních větví
        print(color_text_fore("Доступні вітки:", "green"))
        branches = [branch.name for branch in repo.branches]
        for i, branch in enumerate(branches):
            print(f"    {i + 1}. {branch}")

        # 3. Zobrazení aktuálně aktivní větve
        print(f"\nАктивна вітка: {repo.active_branch.name}")

        # 4. Výběr a přepnutí na větev
        branch_choice = wait_for_input(color_text_fore("Виберіть поточну гілку: ", "green"), timeout = 10)
        branch_choice = branch_choice.strip() if branch_choice else ""

        if not branch_choice:
            if "main" in branches:
                vybrana_vetev = "main"
            else:
                vybrana_vetev = repo.active_branch.name
        elif branch_choice.isdigit():
            branch_index = int(branch_choice) - 1
            if 0 <= branch_index < len(branches):
                vybrana_vetev = branches[branch_index]
            else:
                ConsoleDebug.warn("Неправильне число гілки, використовую активну гілку.")
                vybrana_vetev = repo.active_branch.name
        elif branch_choice in branches:
            vybrana_vetev = branch_choice
        else:
            ConsoleDebug.warn("Невідома гілка, використовую активну гілку.")
            vybrana_vetev = repo.active_branch.name

        print(f"\nПереключаю на вітку: {vybrana_vetev}")

        # Provedení samotného checkoutu
        repo.git.checkout(vybrana_vetev)
        print(color_text_fore("Вітка успішно вибрана!", "green"))
    

    except subprocess.CalledProcessError as e:
        ConsoleDebug.error(f"Chyba při spouštění příkazu git: {e}")
    except FileNotFoundError:
        ConsoleDebug.error("Git nebyl v systému nalezen. Ujistěte se, že je správně nainstalovaný.")
    except TypeError:
        ConsoleDebug.error("Použil jsi asi string místo intengera.")
    except Exception as e:
        ConsoleDebug.error(f"Nastala neočekávaná chyba: {e}")

if __name__ == "__main__": 
    time.sleep(3)
    get_parent_directory()
    variables.get_temp_variables(origin_dir=ORIGIN_DIR, repo_dir=REPO_DIR)
    select_branch()
    auto_git_update.get_directories()

    print(color_text_fore("Запуск авто-оновлення репозиторію...\n", "green"))
    auto_git_update.start(vybrana_vetev, 200)
