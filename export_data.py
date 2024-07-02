
import os
import json
import pandas as pd
import psycopg2
from sshtunnel import SSHTunnelForwarder
from decimal import Decimal
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# SSH and database connection details for database 1
ssh_host1 = os.getenv('SSH_HOST1')
ssh_port1 = int(os.getenv('SSH_PORT1'))
ssh_user1 = os.getenv('SSH_USER1')
ssh_key1 = os.getenv('SSH_KEY1')

db_host1 = os.getenv('DB_HOST1')
db_port1 = int(os.getenv('DB_PORT1'))
db_name1 = os.getenv('DB_NAME1')
db_user1 = os.getenv('DB_USER1')
db_password1 = os.getenv('DB_PASSWORD1')

# SSH and database connection details for database 2
ssh_host2 = os.getenv('SSH_HOST2')
ssh_port2 = int(os.getenv('SSH_PORT2'))
ssh_user2 = os.getenv('SSH_USER2')
ssh_key2 = os.getenv('SSH_KEY2')

db_host2 = os.getenv('DB_HOST2')
db_port2 = int(os.getenv('DB_PORT2'))
db_name2 = os.getenv('DB_NAME2')
db_user2 = os.getenv('DB_USER2')
db_password2 = os.getenv('DB_PASSWORD2')

# SQL scripts directories
sql_scripts_dir1 = 'realisations_sql'  # Путь до директории sql скриптов для реализаций
sql_scripts_dir2 = 'cardcash_sql'  # Путь до директории sql скриптов для кардкешей

# Output directories
output_dir_json = 'output_json'
output_dir_xlsx = 'output_xlsx'

# Ensure output directories exist
os.makedirs(output_dir_json, exist_ok=True)
os.makedirs(output_dir_xlsx, exist_ok=True)

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
            # Store results with the base name of the script as the key
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
        # Extract relevant fields
        serv = [{
            'name': record.pop('name'),
            'price': record.pop('price'),
            'quantity': record.pop('quantity'),
            'sum': record.pop('sum')
        }]
        # Insert 'serv' and reorder keys
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
        elif 'cardcash' in name.lower():
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

def process_database(connection_details, sql_scripts_dir):
    ssh_host, ssh_port, ssh_user, ssh_key, db_host, db_port, db_name, db_user, db_password = connection_details
    
    # Establish SSH tunnel
    with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_pkey=ssh_key,
        remote_bind_address=(db_host, db_port),
        local_bind_address=('localhost', 6543)
    ) as tunnel:
        # Connect to PostgreSQL through the SSH tunnel
        conn = psycopg2.connect(
            host='localhost',
            port=tunnel.local_bind_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

        # Get list of SQL scripts
        sql_scripts = [os.path.join(sql_scripts_dir, f) for f in os.listdir(sql_scripts_dir) if f.endswith('.sql')]

        # Execute SQL scripts and get results
        results = execute_sql_scripts(sql_scripts, conn)

        # Export results to JSON and XLSX
        export_to_json(results, output_dir_json)
        export_to_xlsx(results, output_dir_xlsx)

        # Close the database connection
        conn.close()

def main():
    # Database 1 connection details
    connection_details1 = (ssh_host1, ssh_port1, ssh_user1, ssh_key1, db_host1, db_port1, db_name1, db_user1, db_password1)
    process_database(connection_details1, sql_scripts_dir1)
    
    # Database 2 connection details
    connection_details2 = (ssh_host2, ssh_port2, ssh_user2, ssh_key2, db_host2, db_port2, db_name2, db_user2, db_password2)
    process_database(connection_details2, sql_scripts_dir2)

if __name__ == '__main__':
    main()