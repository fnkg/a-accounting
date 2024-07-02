import re
import os
from datetime import datetime

def update_sql_date(file_path, year, month):
    with open(file_path, 'r') as file:
        sql_script = file.read()

    new_start_date = f"{year}-{month:02d}-01"
    if month == 12:
        new_end_date = f"{year + 1}-01-01"
    else:
        new_end_date = f"{year}-{month + 1:02d}-01"
    
    month_name = datetime(year, month, 1).strftime("%B")

    updated_script = re.sub(r"date >= '\d{4}-\d{2}-\d{2}'", f"date >= '{new_start_date}'", sql_script)
    updated_script = re.sub(r"date < '\d{4}-\d{2}-\d{2}'", f"date < '{new_end_date}'", updated_script)

    # Construct new file name with month name
    new_file_name = re.sub(r' (January|February|March|April|May|June|July|August|September|October|November|December)\.sql$', f' {month_name}.sql', file_path)

    if new_file_name == file_path:
        new_file_name = re.sub(r'\.sql$', f' {month_name}.sql', file_path)

    with open(new_file_name, 'w') as file:
        file.write(updated_script)

    if new_file_name != file_path:
        os.remove(file_path)

    print(f"Updated dates and renamed file to {new_file_name}")

def find_sql_files(directories):
    sql_files = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.sql'):
                    sql_files.append(os.path.join(root, file))
    return sql_files

def update_all_sql_files(directories, year, month):
    sql_files = find_sql_files(directories)
    for sql_file in sql_files:
        update_sql_date(sql_file, year, month)

def main():
    try:
        # Get user input for year and month
        year = int(input("Enter the year (YYYY): "))
        month = int(input("Enter the month (MM): "))

        if month < 1 or month > 12:
            print("Invalid month. Please enter a month between 1 and 12.")
            return
    except ValueError:
        print("Invalid input. Please enter numeric values for year and month.")
        return

    # Directories to search for SQL files
    directories = [
        'realisations_sql',
        'cardcash_sql'
    ]

    # Update all SQL files for the given year and month
    update_all_sql_files(directories, year, month)

if __name__ == "__main__":
    main()