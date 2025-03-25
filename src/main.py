import subprocess
import threading
import itertools
import time
from path_utils import create_directory_structure, select_directory, os
import processing_onlines
import processing_sbp

# Define the base directory as the parent of the `src` directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def loading_indicator(stop_event):
    for frame in itertools.cycle(r'\|/-'):
        if stop_event.is_set():
            break
        print('\rRunning ' + frame, end='', flush=True)
        time.sleep(0.1)
    print('\r08. Running complete!   ')

def run_change_date_sql(year, month, sql_directories):
    script_path = os.path.join(BASE_DIR, "src", "change_date_sql.py")
    for sql_directory in sql_directories:
        result = subprocess.run(["python", script_path, str(year), str(month), sql_directory], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"02. SQL scripts in {sql_directory} processed successfully.")
        else:
            print(f"02. Error processing SQL scripts in {sql_directory}: {result.stderr}")

def run_export_data(temp_dir):
    script_path = os.path.join(BASE_DIR, "src", "export_data.py")
    python_executable = os.path.join(BASE_DIR, ".venv", "Scripts", "python")

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
    script_path = os.path.join(BASE_DIR, "src", "make_readable.py")
    python_executable = os.path.join(BASE_DIR, ".venv", "Scripts", "python")

    print("10. Running make_readable.py")
    print(f"11. Script path: {script_path}")
    print(f"12. Temp directory: {temp_dir}")
    print(f"13. Output directory: {output_dir}")

    result = subprocess.run([python_executable, script_path, temp_dir, output_dir], capture_output=True, text=True)

    if result.returncode == 0:
        print("15. Files processed and saved to readable format successfully.")
    else:
        print(f"15. Error processing files: {result.stderr}")

def main():
    base_path = select_directory("Select the base path where the directory should be created")
    if base_path:
        directory_path, temp_dir, output_dir, year, month = create_directory_structure(base_path)

        # Update the paths for realisations and cardcash directories
        realisations_dir = os.path.join(BASE_DIR, "src", "realisations_sql")
        cardcash_dir = os.path.join(BASE_DIR, "src", "cardcash_sql")

        run_change_date_sql(year, month, [realisations_dir, cardcash_dir])
        run_export_data(temp_dir)

        online_files_path = select_directory("Select the directory containing the online files")
        processing_onlines.process_online_plus(online_files_path, temp_dir)
        processing_onlines.process_online_minus(online_files_path, temp_dir)
        processing_onlines.combine_files(temp_dir)
        processing_onlines.create_json_from_excel(temp_dir, 'onlines.xlsx')

        sbp_files_path = select_directory("Select the directory containing the SBP files")
        processing_sbp.process_all_sbp_files(sbp_files_path, temp_dir)
        
        sbp_files = ['sbp un.xlsx', 'sbp kn.xlsx', 'sbp bs.xlsx', 'sbp mc.xlsx', 'sbp mp.xlsx', 'sbp nr.xlsx']
        for sbp_file in sbp_files:
            processing_sbp.create_json_from_excel(temp_dir, sbp_file)
            
        run_make_readable(temp_dir, output_dir)
    else:
        print("No base directory selected. Exiting.")

if __name__ == "__main__":
    main()
