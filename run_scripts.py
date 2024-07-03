import subprocess
import threading
import itertools
import time
from path_utils import create_directory_structure, select_directory, select_excel_files, os

def loading_indicator(stop_event):
    for frame in itertools.cycle(r'\|/-'):
        if stop_event.is_set():
            break
        print('\rRunning ' + frame, end='', flush=True)
        time.sleep(0.1)
    print('\rRunning complete!   ')

def run_change_date_sql(year, month, sql_directories):
    script_path = "./change_date_sql.py"
    for sql_directory in sql_directories:
        result = subprocess.run(["python", script_path, str(year), str(month), sql_directory], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"SQL scripts in {sql_directory} processed successfully.")
        else:
            print(f"Error processing SQL scripts in {sql_directory}: {result.stderr}")

def run_export_data(archive_dir):
    script_path = os.path.abspath("./export_data.py")
    python_executable = os.path.abspath(os.path.join(".venv", "Scripts", "python"))

    print("Running export_data.py")
    print(f"Using Python executable: {python_executable}")
    print(f"Script path: {script_path}")
    print(f"Archive directory: {archive_dir}")
    print(f"Current working directory: {os.getcwd()}")

    stop_event = threading.Event()
    loading_thread = threading.Thread(target=loading_indicator, args=(stop_event,))
    loading_thread.start()

    result = subprocess.run([python_executable, script_path, archive_dir], capture_output=True, text=True)

    stop_event.set()
    loading_thread.join()

    if result.returncode == 0:
        print("Data exported successfully.")
    else:
        print(f"Error exporting data: {result.stderr}")

if __name__ == "__main__":
    base_path = select_directory("Select the base path where the directory should be created")
    if base_path:
        directory_path, archive_dir, year, month = create_directory_structure(base_path)

        realisations_dir = os.path.abspath("realisations_sql")
        cardcash_dir = os.path.abspath("cardcash_sql")

        run_change_date_sql(year, month, [realisations_dir, cardcash_dir])
        run_export_data(archive_dir)
        
        excel_files = select_excel_files("Select Excel files for processing Online and SBP")
        print(f"Selected Excel files: {excel_files}")
    else:
        print("No base directory selected. Exiting.")
