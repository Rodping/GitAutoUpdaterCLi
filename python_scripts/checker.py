import os

try:
    import python_scripts.variables as variables
except Exception as e:
    print(f"Loading components failed, error: {e}")
    import variables

ORIGIN_DIR = ""
TEMP_DIR = ""
CONTENT_DIR = ""
SCRIPTS_DIR = ""
REPO_DIR = ""

def python_file_check(_DIR, _TEMP_DIR):
    total_files = 0
    total_python_files = 0
    
    # Reads all folders and files and copies Python files
    for root, subdirectories, files in os.walk(_DIR):
        for file_name in files:
            total_files += 1
            file_path = os.path.join(root, file_name)
            
            # 1. Check .py extension
            if file_name.endswith('.py'):
                print(f"[Python (.py)] {file_path}")
                total_python_files += 1
            else:
                continue

            MyPathlib = os.path
            # 2. Store .py files
            try:
                # Open the .py script
                with open(file_path, 'r', encoding='utf-8') as r:
                    
                    text = r.read() # Reads the script and writes it
                    
                    rel_path_in_temp = os.path.relpath(file_path, start=_DIR)
                    temp_file_folder = os.path.join(_TEMP_DIR, rel_path_in_temp)
                    temp_file_dir = os.path.dirname(temp_file_folder)
                    if temp_file_dir:
                        os.makedirs(temp_file_dir, exist_ok=True)

                    with open(temp_file_folder, 'w', encoding='utf-8') as w:
                        w.write(text)
                    

            except Exception:
                # Skip binary files, access errors, etc.
                continue
            # 3 read
    print("-" * 40)
    print(f"Total files checked: {total_files}")
    print(f"Python files among them: {total_python_files}")

def get_directories():
    global ORIGIN_DIR, TEMP_DIR, TEMP_FILE, TEMP_FILE_NAME, CONTENT_DIR, SCRIPTS_DIR, REPO_DIR, Directories
    Directories = variables.get_temp_variables(origin_dir=ORIGIN_DIR or None, repo_dir=REPO_DIR or None)  # type: ignore
    ORIGIN_DIR = Directories.ORIGIN_DIR
    TEMP_DIR = Directories.TEMP_DIR 
    CONTENT_DIR = Directories.CONTENT_DIR 
    SCRIPTS_DIR = Directories.SCRIPTS_DIR 
    REPO_DIR = Directories.REPO_DIR 


if __name__ == "__main__":
    print("Starting copy...\n")
    get_directories()

    python_file_check(ORIGIN_DIR, TEMP_DIR)