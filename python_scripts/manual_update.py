import auto_git_update_5min as auto_git_update
import os
import sys

if __name__ == "__main__":
    ORIGIN_DIR = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(ORIGIN_DIR)
    try:
        import StartAutoUpdate
    finally:
        if ORIGIN_DIR in sys.path:
            sys.path.remove(ORIGIN_DIR)

    StartAutoUpdate.select_branch()
    vybrana_vetev = StartAutoUpdate.vybrana_vetev
    auto_git_update.update_repo(ORIGIN_DIR, vybrana_vetev)