import pandas as pd
import os
import json

def process_online_plus(input_dir, output_dir):
    file_path = os.path.join(input_dir, '+online.csv')
    output_path = os.path.join(output_dir, 'online_plus.xlsx')
    
    df = pd.read_csv(file_path, delimiter=';')
    
    print("Column names in the CSV file:", df.columns.tolist())
    
    try:
        df['id'] = df['Идентификатор платежа'].astype(str) + '1'
        df['date'] = pd.to_datetime(df['Дата платежа']).dt.strftime('%Y%m%d')
        df['sum'] = df['Сумма платежа'].str.replace(',', '.').astype(float)
        df['type'] = 'online'
        df['store_uuid'] = '720b6201-a0c4-11e1-9f3c-001e37ed2a0b'
        df['company_uuid'] = '4d0460ff-a0cb-11e2-9494-91acf06830ea'
        
        df = df[['id', 'date', 'sum', 'type', 'store_uuid', 'company_uuid']]
        
        df.to_excel(output_path, index=False)
        print(f"File saved successfully to {output_path}")
    except KeyError as e:
        print(f"Error: {e}. Please check the column names in your CSV file.")

def process_online_minus(input_dir, output_dir):
    file_path = os.path.join(input_dir, '-online.csv')
    output_path = os.path.join(output_dir, 'online_minus.xlsx')
    
    df = pd.read_csv(file_path, delimiter=';')
    
    print("Column names in the CSV file:", df.columns.tolist())
    
    month_filter = input("Enter the month (MM format) to filter by: ")
    
    try:
        df['id'] = df['Идентификатор платежа'].astype(str) + '1'
        df['date'] = pd.to_datetime(df['Дата возврата (если возвратов несколько — последнего)']).dt.strftime('%Y%m%d')
        
        df['Сумма возврата по платежу'] = df['Сумма возврата по платежу'].str.replace('RUB', '').str.strip()
        df['Сумма возврата по платежу'] = df['Сумма возврата по платежу'].str.replace(',', '.')
        df['sum'] = df['Сумма возврата по платежу'].astype(float) * -1
        
        df['type'] = 'online'
        df['store_uuid'] = '720b6201-a0c4-11e1-9f3c-001e37ed2a0b'
        df['company_uuid'] = '4d0460ff-a0cb-11e2-9494-91acf06830ea'
        
        df['month'] = pd.to_datetime(df['Дата возврата (если возвратов несколько — последнего)']).dt.strftime('%m')
        
        df = df[['id', 'date', 'sum', 'type', 'store_uuid', 'company_uuid', 'month']]
        
        df_filtered = df[df['month'] == month_filter]
        
        df_filtered.to_excel(output_path, index=False)
        print(f"File saved successfully to {output_path}")
    except KeyError as e:
        print(f"Error: {e}. Please check the column names in your CSV file.")
    except ValueError as e:
        print(f"Error: {e}. There was an issue converting data to float.")

def combine_files(output_dir):
    plus_df = pd.read_excel(os.path.join(output_dir, 'online_plus.xlsx'))
    minus_df = pd.read_excel(os.path.join(output_dir, 'online_minus.xlsx'))
    
    minus_df_positive = minus_df.copy()
    minus_df_positive['sum'] = minus_df_positive['sum'].abs()
    
    combined_df = pd.concat([plus_df, minus_df.drop(columns=['month']), minus_df_positive.drop(columns=['month'])], ignore_index=True)
    
    combined_output_path = os.path.join(output_dir, 'onlines.xlsx')
    combined_df.to_excel(combined_output_path, index=False)
    
    print(f"Combined file saved successfully to {combined_output_path}")

def create_json_from_excel(output_dir, filename):
    combined_df = pd.read_excel(os.path.join(output_dir, filename))
    
    combined_df['date'] = combined_df['date'].astype(str)
    combined_df['sum'] = combined_df['sum'].astype(float)
    
    json_data = {"payments": combined_df.to_dict(orient='records')}
    
    json_output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.json")
    with open(json_output_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)
    
    print(f"JSON file saved successfully to {json_output_path}")