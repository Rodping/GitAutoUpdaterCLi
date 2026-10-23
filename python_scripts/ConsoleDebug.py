import colorama
from colorama import Fore, Back, Style
import inspect
import os

def message(text: str = "message from code"):
    caller = inspect.stack()[1]
    print(Fore.WHITE + f"Message (from {os.path.basename(caller.filename)} line {caller.lineno}): " + text + Style.RESET_ALL)
def warn(text: str = "Warning from code"):
    caller = inspect.stack()[1]
    print(Fore.YELLOW + f"Warning! (from {os.path.basename(caller.filename)} line {caller.lineno}): " + text + Style.RESET_ALL)
def error(text):
    caller = inspect.stack()[1]
    print(Fore.RED + f"Error! (from {os.path.basename(caller.filename)} line {caller.lineno}): " + text + Style.RESET_ALL)

if __name__ == "__main__": 
    message("test message - test node")
    warn("Very bad promblem - 2+2≠4")
    error("Git not working")
