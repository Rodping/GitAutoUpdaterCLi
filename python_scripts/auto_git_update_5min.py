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
    print(f"Loading components failed, error: {e}")
    import checker
    import variables
# --- SETTINGS ---
# SSH URL (recommended) or HTTPS URL with a token
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

# Interval in seconds (5 minutes = 300 seconds)

########## func ###########
def color_text_fore(text: str, color: str):
    color_code = getattr(Fore, color.upper(), Fore.WHITE)
    return(color_code + text + Style.RESET_ALL)

def update_repo(TARGET_DIR, selected_branch):
    if not TARGET_DIR:
        raise ValueError("REPO_DIR is not set. Make sure setup_directories() is called before start().")
    
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(color_text_fore(f"[{current_time}] Synchronizing...", "green"))

    TEMP_DIR = os.path.abspath(os.path.join(os.path.dirname(TARGET_DIR), "temp"))

    #repo.git.checkout(selected_branch)
    try:
        # Check whether the .git folder already exists
        if os.path.exists(os.path.join(TARGET_DIR, ".git")):
            print("Repository found, updating...")
            # Runs 'git pull' directly in the target directory
            subprocess.run(["git", "pull"], cwd=TARGET_DIR, check=True)

        else:
            print("Repository not found, cloning...")
            os.makedirs(TARGET_DIR, exist_ok=True)
            subprocess.run(["git", "clone", REPO_URL, TARGET_DIR], check=True)

        print("-> Done. All files are updated.")

        # repo = git.Repo(TARGET_DIR)
        # repo.git.checkout(selected_branch)
        # repo.git.pull()
        print(f"-> Selected '{selected_branch}' branch for use.\n")

    except subprocess.CalledProcessError as e:
        print(f"-> ERROR: Git command failed: {e}\n")
    except Exception as e:
        print(f"-> UNEXPECTED ERROR: {e}\n")

    # checker.python_file_check(ORIGIN_DIR, TEMP_DIR)
    



def start(branch, interval=300):
    # import variables
    global ORIGIN_DIR, isrunning, REPO_DIR, actual_branch, cycle_count

    INTERVAL = interval
    actual_branch = branch
    TempVars = variables.get_temp_variables(origin_dir=ORIGIN_DIR or None, repo_dir=REPO_DIR or None)

    if INTERVAL % 60 == 0:
        interval_text = f"{INTERVAL // 60} minutes"
    else:
        interval_text = f"{INTERVAL} seconds"
    print(f"AutoUpdate started. The check will run every {interval_text}.")
    print("Press Ctrl+C to exit.\n")

    isrunning = True
    actual_cycle_count = cycle_count
    try:
        while True:
            if isrunning:
                if cycle_count > actual_cycle_count:
                    break  # If the cycle count changes, stop the loop
                update_repo(REPO_DIR, branch)
                time.sleep(INTERVAL)
            else:
                time.sleep(1)  # Short pause to avoid unnecessary CPU load
            
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
    print("Run StartServer.py instead of auto_git_update_5min.py")
    exit(1)