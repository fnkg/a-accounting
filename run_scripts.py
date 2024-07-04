import subprocess
import threading
import itertools
import time
from path_utils import create_directory_structure, select_directory, os

def loading_indicator(stop_event):
    for frame in itertools.cycle(r'\|/-'):
        if stop_event.is_set():
            break
        print('\rRunning ' + frame, end='', flush=True)
        time.sleep(0.1)
    print('\r08. Running complete!   ')

def run_change_date_sql(year, month, sql_directories):
    script_path = "./change_date_sql.py"
    for sql_directory in sql_directories:
        result = subprocess.run(["python", script_path, str(year), str(month), sql_directory], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"02. SQL scripts in {sql_directory} processed successfully.")
        else:
            print(f"02. Error processing SQL scripts in {sql_directory}: {result.stderr}")

def run_export_data(temp_dir):
    script_path = os.path.abspath("./export_data.py")
    python_executable = os.path.abspath(os.path.join(".venv", "Scripts", "python"))

    print("03. Running export_data.py")
    print(f"04. Using Python executable: {python_executable}")
    print(f"05. Script path: {script_path}")
    print(f"06. Temp directory: {temp_dir}")
    print(f"07. Current working directory: {os.getcwd()}")

    stop_event = threading.Event()
    loading_thread = threading.Thread(target=loading_indicator, args=(stop_event,))
    loading_thread.start()

    result = subprocess.run([python_executable, script_path, temp_dir], capture_output=True, text=True)

    stop_event.set()
    loading_thread.join()

    if result.returncode == 0:
        print("09. Data exported successfully.")
    else:
        print(f"09. Error exporting data: {result.stderr}")

def run_make_readable(temp_dir, output_dir):
    script_path = os.path.abspath("./make_readable.py")
    python_executable = os.path.abspath(os.path.join(".venv", "Scripts", "python"))

    print("10. Running make_readable.py")
    print(f"11. Script path: {script_path}")
    print(f"12. Temp directory: {temp_dir}")
    print(f"13. Output directory: {output_dir}")

    result = subprocess.run([python_executable, script_path, temp_dir, output_dir], capture_output=True, text=True)

    if result.returncode == 0:
        print("15. Files processed and saved to readable format successfully.")
    else:
        print(f"15. Error processing files: {result.stderr}")

if __name__ == "__main__":
    base_path = select_directory("Select the base path where the directory should be created")
    if base_path:
        directory_path, temp_dir, output_dir, year, month = create_directory_structure(base_path)

        realisations_dir = os.path.abspath("realisations_sql")
        cardcash_dir = os.path.abspath("cardcash_sql")

        run_change_date_sql(year, month, [realisations_dir, cardcash_dir])
        run_export_data(temp_dir)
        run_make_readable(temp_dir, output_dir)
    else:
        print("No base directory selected. Exiting.")
