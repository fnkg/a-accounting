# path_utils.py
import os
from datetime import datetime
from tkinter import Tk, filedialog, simpledialog

def create_directory_structure(base_path):
    root = Tk()
    root.withdraw()

    year = simpledialog.askstring("Input", "Enter the year (YYYY):", parent=root)
    month = simpledialog.askstring("Input", "Enter the month (MM):", parent=root)

    root.destroy()

    month_name = datetime.strptime(month, "%m").strftime("%B")
    directory_name = f"{year}-{month} {month_name}"
    directory_path = os.path.join(base_path, directory_name)

    os.makedirs(directory_path, exist_ok=True)
    subdirectories = ["readable", "loadable", "temp"]
    for subdirectory in subdirectories:
        os.makedirs(os.path.join(directory_path, subdirectory), exist_ok=True)

    print(f"Directory structure created at {directory_path}")
    return directory_path, os.path.join(directory_path, "temp"), int(year), int(month)

def select_directory(prompt):
    root = Tk()
    root.withdraw()
    selected_directory = filedialog.askdirectory(title=prompt)
    root.destroy()
    return selected_directory

# def select_excel_files(prompt):
#     root = Tk()
#     root.withdraw()
#     selected_files = filedialog.askopenfilenames(title=prompt, filetypes=[("Excel files", "*.xlsx *.xls *.csv")])
#     root.destroy()
#     return selected_files
