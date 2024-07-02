import pandas as pd

def process_excel(input_excel_path, output_excel_path, store_uuid_mapping):
    df = pd.read_excel(input_excel_path)
    columns_to_drop = ['inn', 'onlyinvoice', 'price', 'quantity', 'company_uuid']
    df.drop(columns=columns_to_drop, inplace=True)
    df['store_uuid'] = df['store_uuid'].map(store_uuid_mapping)
    df.to_excel(output_excel_path, index=False)
    print(f"Processed Excel saved to {output_excel_path}")

def process_all_excel_files(excel_files, store_uuid_mapping):
    for excel_file in excel_files:
        output_file = excel_file.replace(".xlsx", " readable.xlsx")
        process_excel(excel_file, output_file, store_uuid_mapping)

# List of XLSX file paths
excel_files = [
    'Result_1.xlsx',
]

# Store UUID mapping
store_uuid_mapping = {
    "f966000c-3c48-11dd-96d9-000c6e46fcad": "UN",
    "823cd454-cab4-11eb-a20a-00155dc42e00": "KN",
    "e884414e-345f-11e2-9222-f23cea8074d9": "MC",
    "608fadf8-9055-11e2-ba2e-f1630d599bdb": "BS",
    "e8844150-345f-11e2-9222-f23cea8074d9": "MP",
    "e8844153-345f-11e2-9222-f23cea8074d9": "RG",
    "720b6201-a0c4-11e1-9f3c-001e37ed2a0b": "online",
}

# Process all XLSX files
process_all_excel_files(excel_files, store_uuid_mapping)
