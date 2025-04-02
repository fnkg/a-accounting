import os
from datetime import datetime
from tkinter import Tk, filedialog, simpledialog

def create_directory_structure(base_path, year, month):
    month_name = datetime.strptime(str(month), "%m").strftime("%B")
    directory_name = f"{year}-{month:02d} {month_name}"
    directory_path = os.path.join(base_path, directory_name)

    os.makedirs(directory_path, exist_ok=True)
    subdirectories = ["readable", "loadable", "temp"]
    for subdirectory in subdirectories:
        os.makedirs(os.path.join(directory_path, subdirectory), exist_ok=True)

    print(f"01. Directory structure created at {directory_path}")
    return directory_path, os.path.join(directory_path, "temp"), os.path.join(directory_path, "readable")


def select_directory(prompt):
    root = Tk()
    root.withdraw()
    selected_directory = filedialog.askdirectory(title=prompt)
    root.destroy()
    return selected_directory