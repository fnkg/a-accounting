import pandas as pd
import openpyxl
import json

def process_online_plus():
    # Static file path for debugging
    file_path = './onlines/+online.csv'
    output_path = './onlines/online_plus.xlsx'
    
    # Load the CSV file with correct delimiter
    df = pd.read_csv(file_path, delimiter=';')
    
    # Print column names for debugging
    print("Column names in the CSV file:", df.columns.tolist())
    
    # Apply formulas to the columns using the specified column names
    try:
        df['id'] = df['Идентификатор платежа'].astype(str) + '1'
        df['date'] = pd.to_datetime(df['Дата платежа']).dt.strftime('%Y%m%d')
        df['sum'] = df['Сумма платежа'].str.replace(',', '.').astype(float)
        df['type'] = 'online'
        df['store_uuid'] = '720b6201-a0c4-11e1-9f3c-001e37ed2a0b'
        df['company_uuid'] = '4d0460ff-a0cb-11e2-9494-91acf06830ea'
        
        # Select and reorder columns
        df = df[['id', 'date', 'sum', 'type', 'store_uuid', 'company_uuid']]
        
        # Save the DataFrame to an Excel file
        df.to_excel(output_path, index=False)
        
        print(f"File saved successfully to {output_path}")
    except KeyError as e:
        print(f"Error: {e}. Please check the column names in your CSV file.")

def process_online_minus():
    # Static file path for debugging
    file_path = './onlines/-online.csv'
    output_path = './onlines/online_minus.xlsx'
    
    # Load the CSV file with correct delimiter
    df = pd.read_csv(file_path, delimiter=';')
    
    # Print column names for debugging
    print("Column names in the CSV file:", df.columns.tolist())
    
    # Get month filter from user input
    month_filter = input("Enter the month (MM format) to filter by: ")
    
    # Apply formulas to the columns using the specified column names
    try:
        df['id'] = df['Идентификатор платежа'].astype(str) + '1'
        df['date'] = pd.to_datetime(df['Дата возврата (если возвратов несколько — последнего)']).dt.strftime('%Y%m%d')
        
        # Clean and negate sum
        df['Сумма возврата по платежу'] = df['Сумма возврата по платежу'].str.replace('RUB', '').str.strip()
        df['Сумма возврата по платежу'] = df['Сумма возврата по платежу'].str.replace(',', '.')
        df['sum'] = df['Сумма возврата по платежу'].astype(float) * -1
        
        df['type'] = 'online'
        df['store_uuid'] = '720b6201-a0c4-11e1-9f3c-001e37ed2a0b'
        df['company_uuid'] = '4d0460ff-a0cb-11e2-9494-91acf06830ea'
        
        # Extract month
        df['month'] = pd.to_datetime(df['Дата возврата (если возвратов несколько — последнего)']).dt.strftime('%m')
        
        # Select and reorder columns
        df = df[['id', 'date', 'sum', 'type', 'store_uuid', 'company_uuid', 'month']]
        
        # Filter by month
        df_filtered = df[df['month'] == month_filter]
        
        # Save the filtered DataFrame to an Excel file
        df_filtered.to_excel(output_path, index=False)
        
        print(f"File saved successfully to {output_path}")
    except KeyError as e:
        print(f"Error: {e}. Please check the column names in your CSV file.")
    except ValueError as e:
        print(f"Error: {e}. There was an issue converting data to float.")

def combine_files():
    # Load the processed files
    plus_df = pd.read_excel('./onlines/online_plus.xlsx')
    minus_df = pd.read_excel('./onlines/online_minus.xlsx')
    
    # Duplicate minus_df with positive sum
    minus_df_positive = minus_df.copy()
    minus_df_positive['sum'] = minus_df_positive['sum'].abs()
    
    # Combine all dataframes
    combined_df = pd.concat([plus_df, minus_df.drop(columns=['month']), minus_df_positive.drop(columns=['month'])], ignore_index=True)
    
    # Save the combined DataFrame to a new Excel file
    combined_output_path = './onlines.xlsx'
    combined_df.to_excel(combined_output_path, index=False)
    
    print(f"Combined file saved successfully to {combined_output_path}")

def create_json_from_excel():
    # Load the combined Excel file
    combined_df = pd.read_excel('./onlines.xlsx')
    
    # Ensure correct data types
    combined_df['date'] = combined_df['date'].astype(str)
    combined_df['sum'] = combined_df['sum'].astype(float)
    
    # Create the JSON structure
    json_data = {"payments": combined_df.to_dict(orient='records')}
    
    # Save the JSON data to a file
    json_output_path = './onlines.json'
    with open(json_output_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)
    
    print(f"JSON file saved successfully to {json_output_path}")

# Example usage
process_online_plus()
process_online_minus()
combine_files()
create_json_from_excel()
