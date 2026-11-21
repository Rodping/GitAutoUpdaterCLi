import argparse
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
# import keyboard # Only for computers
"""

StarterServer.py must always be in the /PlastHub/ folder,
otherwise the whole system breaks.

Folder names:
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
def color_text_foreground(text: str, color: str):
    color_code = getattr(Fore, color.upper(), Fore.WHITE)
    return(color_code + text + Style.RESET_ALL)

path = os.path

# def wait_for_input
input_received = False
waiting_for_input = False
input_text = ""
input_text_final = ""
###########################

ORIGIN_DIR = path.dirname(__file__) # - Origin root folder, where the StarterServer.py is located
REPO_DIR = ""
SCRIPTS_DIR = path.join(ORIGIN_DIR, "python-scripts")

print(color_text_foreground("Server folder: ", "green") + ORIGIN_DIR)
selected_branch = ""

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
        time.sleep(0.1) # Short pause to avoid unnecessary CPU load
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

def get_parent_directory(test_mode=False):
    global ORIGIN_DIR, REPO_DIR

    # 1. Choose a folder to save to
    if test_mode:
        print(color_text_foreground("Test mode enabled: using local repo folder.", "yellow"))
        REPO_DIR = path.join(ORIGIN_DIR, "local-test-repo")
        os.makedirs(REPO_DIR, exist_ok=True)
    else:
        with open(os.path.join(ORIGIN_DIR, "config.txt"), "r") as config_file:
            config_lines = config_file.readlines()
            for line in config_lines:
                if line.startswith("REPO_DIR="):
                    configured_repo_dir = line.split("=", 1)[1].strip()
                    local_path = configured_repo_dir.replace("\\", "/")
                    if local_path == "local":
                        REPO_DIR = ORIGIN_DIR
                    elif local_path.startswith("local/"):
                        local_subpath = local_path[len("local/"):]
                        REPO_DIR = path.join(ORIGIN_DIR, *local_subpath.split("/"))
                    else:
                        REPO_DIR = configured_repo_dir
                    break
        #text_for_dir_quest = (r"Specify the path to the folder (if you leave it empty, it will save to '..\repo\' )" +
        #                       "\n------> ")
        #REPO_DIR = wait_for_input(text_for_dir_quest, timeout = 10)
    
    
    if(not REPO_DIR):
        # ORIGIN_DIR = os.path.dirname(__file__) 
        print(color_text_foreground("Cannot determine the folder, so I am using the test folder!!!", "red"))
        REPO_DIR = path.join(ORIGIN_DIR, "local-test-repo")

    print(color_text_foreground("\nUsing folder: ", "green") + REPO_DIR)

def select_branch():
    global REPO_DIR, selected_branch
    # 2. Choose the branch to copy
    try:
        # 0. Check whether this is a valid repository
        if not os.path.exists(os.path.join(REPO_DIR, ".git")):
            ConsoleDebug.message("Empty folder: repository does not exist. I am skipping branch selection and allowing the repository to download.")
            selected_branch = ""
            return
        # --- Git safe.directory fix for Android ---
        git.Git().config("--global", "--add", "safe.directory", REPO_DIR)
        # -----------------------------------------------

        # 1. Open an existing repository (enter the path to your project)
        repo = git.Repo(REPO_DIR)

        # 2. Print all local branches
        print(color_text_foreground("Available branches:", "green"))
        branches = [branch.name for branch in repo.branches]
        for i, branch in enumerate(branches):
            print(f"    {i + 1}. {branch}")

        # 3. Show the currently active branch
        print(f"\nActive branch: {repo.active_branch.name}")

        # 4. Select and switch to a branch
        branch_choice = wait_for_input(color_text_foreground("Select the current branch: ", "green"), timeout = 15)
        branch_choice = branch_choice.strip() if branch_choice else ""

        if not branch_choice:
            if "main" in branches:
                selected_branch = "main"
            else:
                selected_branch = repo.active_branch.name
        elif branch_choice.isdigit():
            branch_index = int(branch_choice) - 1
            if 0 <= branch_index < len(branches):
                selected_branch = branches[branch_index]
            else:
                ConsoleDebug.warn("Invalid branch number, using the active branch.")
                selected_branch = repo.active_branch.name
        elif branch_choice in branches:
            selected_branch = branch_choice
        else:
            ConsoleDebug.warn("Unknown branch, using the active branch.")
            selected_branch = repo.active_branch.name

        print(f"\nSwitching to branch: {selected_branch}")

        # Perform the checkout itself
        repo.git.checkout(selected_branch)
        print(color_text_foreground("Branch selected successfully!", "green"))
    

    except subprocess.CalledProcessError as e:
        ConsoleDebug.error(f"Error while running git command: {e}")
    except FileNotFoundError:
        ConsoleDebug.error("Git was not found in the system. Make sure it is installed correctly.")
    except TypeError:
        ConsoleDebug.error("You probably used a string instead of an integer.")
    except Exception as e:
        ConsoleDebug.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description="Start the repository auto-updater.")
    parser.add_argument("-test", "--test", action="store_true",
                        help="use the local repo folder instead of prompting for a path")
    args = parser.parse_args()

    time.sleep(3)
    get_parent_directory(test_mode=args.test)
    variables.get_temp_variables(origin_dir=ORIGIN_DIR, repo_dir=REPO_DIR)
    select_branch()
    auto_git_update.get_directories()

    print(color_text_foreground("Starting repository auto-update...\n", "green"))
    auto_git_update.start(selected_branch, 200)
