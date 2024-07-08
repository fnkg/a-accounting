import pandas as pd
import os
import json

def get_legal_entity_info(filename):
    if 'bg' in filename:
        store_uuid = '720b6201-a0c4-11e1-9f3c-001e37ed2a0b'
        company_uuid = 'c84cdf1b-6720-11ed-a221-00155d59dd05'
    elif 'kacha' in filename:
        store_uuid = '720b6201-a0c4-11e1-9f3c-001e37ed2a0b'
        company_uuid = '7dbfb2a3-6721-11ed-a221-00155d59dd05'
    elif 'kch' in filename:
        store_uuid = '97b66876-45fc-11e3-a6a8-c2b5fc6ba0c4'
        company_uuid = '4d0460ff-a0cb-11e2-9494-91acf06830ea'
    elif 'mp' in filename:
        store_uuid = '720b6201-a0c4-11e1-9f3c-001e37ed2a0b'
        company_uuid = '805250f1-2309-11ef-a230-00155d59dd05'
    elif 'nr' in filename:
        store_uuid = '720b6201-a0c4-11e1-9f3c-001e37ed2a0b'
        company_uuid = '4557b547-348d-11ef-a230-00155d59dd05'
    else:
        raise ValueError(f"Unknown legal entity in filename: {filename}")
    
    return store_uuid, company_uuid

def process_sbp_file(file_path, output_dir):
    df = pd.read_csv(file_path, delimiter=';')
    filename = os.path.splitext(os.path.basename(file_path))[0]
    store_uuid, company_uuid = get_legal_entity_info(filename)

    try:
        df['id'] = df['id заказа'].astype(str) + '1'
        df['date'] = pd.to_datetime(df['Дата операции МСК'], dayfirst=True).dt.strftime('%Y%m%d')
        
        df['sum'] = df['Сумма'].astype(str).str.replace(',', '.').astype(float)
        df['type'] = 'online'
        df['store_uuid'] = store_uuid
        df['company_uuid'] = company_uuid
        
        df = df[['id', 'date', 'sum', 'type', 'store_uuid', 'company_uuid']]
        
        output_path = os.path.join(output_dir, f"{filename}.xlsx")
        
        df.to_excel(output_path, index=False)
        
        print(f"File saved successfully to {output_path}")
    except KeyError as e:
        print(f"Error: {e}. Please check the column names in your CSV file.")
    except ValueError as e:
        print(f"Error: {e}. There was an issue with the data.")

def process_all_sbp_files(input_dir, output_dir):
    sbp_files = ['sbp bg.csv', 'sbp kacha.csv', 'sbp kch.csv', 'sbp mp.csv', 'sbp nr.csv']

    for sbp_file in sbp_files:
        file_path = os.path.join(input_dir, sbp_file)
        process_sbp_file(file_path, output_dir)

def create_json_from_excel(output_dir, filename):
    combined_df = pd.read_excel(os.path.join(output_dir, filename))
    
    combined_df['date'] = combined_df['date'].astype(str)
    combined_df['sum'] = combined_df['sum'].astype(float)
    
    json_data = {"payments": combined_df.to_dict(orient='records')}

    json_output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.json")
    with open(json_output_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)
    
    print(f"JSON file saved successfully to {json_output_path}")