import os

try:
    import python_scripts.variables as variables
except Exception as e:
    print(f"Загрузка компонентів не пішла, помилка: {e}")
    import variables

ORIGIN_DIR = ""
TEMP_DIR = ""
CONTENT_DIR = ""
SCRIPTS_DIR = ""
REPO_DIR = ""

def python_file_check(_DIR, _TEMP_DIR):
    pocet_celkem = 0
    pocet_python = 0
    
    # Читає всі папки та файли і копіює пайтон файли
    for koren, podslozky, soubory in os.walk(_DIR):
        for soubor in soubory:
            pocet_celkem += 1
            cesta_k_souboru = os.path.join(koren, soubor)
            
            # 1. Kontrola přípony .py
            if soubor.endswith('.py'):
                print(f"[Python (.py)] {cesta_k_souboru}")
                pocet_python += 1
            else:
                continue

            MyPathlib = os.path
            # 2. Зберігання файлів .py
            try:
                # відкриє скрипт .py
                with open(cesta_k_souboru, 'r', encoding='utf-8') as r:
                    
                    text = r.read() # Читає скріпт і записує
                    
                    rel_cesta_v_temp = os.path.relpath(cesta_k_souboru, start=_DIR)
                    temp_file_folder = os.path.join(_TEMP_DIR, rel_cesta_v_temp)
                    temp_file_dir = os.path.dirname(temp_file_folder)
                    if temp_file_dir:
                        os.makedirs(temp_file_dir, exist_ok=True)

                    with open(temp_file_folder, 'w', encoding='utf-8') as w:
                        w.write(text)
                    

            except Exception:
                # Přeskočení binárních souborů, chyb přístupu apod.
                continue
            # 3 čtení
    print("-" * 40)
    print(f"Celkem zkontrolováno souborů: {pocet_celkem}")
    print(f"Z toho Python souborů: {pocet_python}")

def get_directories():
    global ORIGIN_DIR, TEMP_DIR, TEMP_FILE, TEMP_FILE_NAME, CONTENT_DIR, SCRIPTS_DIR, REPO_DIR, Directories
    Directories = variables.get_temp_variables(origin_dir=ORIGIN_DIR or None, repo_dir=REPO_DIR or None)  # type: ignore
    ORIGIN_DIR = Directories.ORIGIN_DIR
    TEMP_DIR = Directories.TEMP_DIR 
    CONTENT_DIR = Directories.CONTENT_DIR 
    SCRIPTS_DIR = Directories.SCRIPTS_DIR 
    REPO_DIR = Directories.REPO_DIR 


if __name__ == "__main__":
    print("Запуск копіювання...\n")
    get_directories()

    python_file_check(ORIGIN_DIR, TEMP_DIR)