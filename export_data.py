import sys
import os
import json
import pandas as pd
from decimal import Decimal
from db_utils import create_db_connection, close_db_connection, get_connection_details

def execute_sql_scripts(sql_scripts, connection):
    results = {}
    for script in sql_scripts:
        with open(script, 'r', encoding='utf-8') as file:
            sql_query = file.read()
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(data, columns=columns)
            base_name = os.path.basename(script).replace('.sql', '')
            results[base_name] = df
    return results

def convert_decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def process_realisations(df):
    records = df.to_dict(orient='records')
    for record in records:
        serv = [{
            'name': record.pop('name'),
            'price': record.pop('price'),
            'quantity': record.pop('quantity'),
            'sum': record.pop('sum')
        }]
        new_record = {
            'date': record['date'],
            'inn': record['inn'],
            'onlyinvoice': record['onlyinvoice'],
            'serv': serv,
            'store_uuid': record['store_uuid'],
            'company_uuid': record['company_uuid']
        }
        record.clear()
        record.update(new_record)
    return records

def process_cardcash(df):
    return {"payments": df.to_dict(orient='records')}

def export_to_json(dataframes, output_dir):
    for name, df in dataframes.items():
        if 'realisation' in name.lower():
            data = process_realisations(df)
        elif 'card+cash' in name.lower():
            data = process_cardcash(df)
        else:
            data = df.to_dict(orient='records')
        output_file = os.path.join(output_dir, f'{name}.json')
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, default=convert_decimal_to_float, ensure_ascii=False)
        print(f'Data exported to {output_file}')

def format_floats(df):
    for col in ['price', 'sum']:
        if col in df.columns:
            df[col] = df[col].astype(float)
    return df

def export_to_xlsx(dataframes, output_dir):
    for name, df in dataframes.items():
        if 'realisation' in name.lower():
            df = format_floats(df)
        output_file = os.path.join(output_dir, f'{name}.xlsx')
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=name, index=False)
        print(f'Data exported to {output_file}')

def process_database(db_number, sql_scripts_dir, temp_dir):
    connection_details = get_connection_details(db_number)
    tunnel, conn = create_db_connection(connection_details)
    
    try:
        sql_scripts = [os.path.join(sql_scripts_dir, f) for f in os.listdir(sql_scripts_dir) if f.endswith('.sql')]
        results = execute_sql_scripts(sql_scripts, conn)
        export_to_json(results, temp_dir)
        export_to_xlsx(results, temp_dir)
    except Exception as e:
        print(f"Error processing database: {e}")
    finally:
        close_db_connection(tunnel, conn)

def main():
    if len(sys.argv) != 2:
        print("Usage: python export_data.py <temp_directory>")
        return
    
    temp_dir = sys.argv[1]

    realisations_sql_directory = os.path.abspath("realisations_sql")
    cardcash_sql_directory = os.path.abspath("cardcash_sql")

    process_database(1, realisations_sql_directory, temp_dir)
    process_database(2, cardcash_sql_directory, temp_dir)

if __name__ == '__main__':
    main()