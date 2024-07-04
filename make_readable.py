import pandas as pd
import os
import sys

def process_excel(input_excel_path, output_excel_path, columns_to_drop, store_uuid_mapping):
    df = pd.read_excel(input_excel_path)
    df.drop(columns=columns_to_drop, inplace=True)
    df['store_uuid'] = df['store_uuid'].map(store_uuid_mapping)
    df.to_excel(output_excel_path, index=False)
    print(f"Processed Excel saved to {output_excel_path}")

def process_files(excel_files, columns_to_drop, store_uuid_mapping, output_dir):
    for excel_file in excel_files:
        output_file = os.path.join(output_dir, os.path.basename(excel_file).replace(".xlsx", " readable.xlsx"))
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        process_excel(excel_file, output_file, columns_to_drop, store_uuid_mapping)

def process_all_excel_files(excel_dir, store_uuid_mapping, output_dir):
    realisation_files = []
    cardcash_files = []
    online_files = []
    sbp_files = []

    for root, dirs, files in os.walk(excel_dir):
        for file in files:
            if file.endswith(".xlsx"):
                if "realisation" in file:
                    realisation_files.append(os.path.join(root, file))
                elif "card+cash" in file:
                    cardcash_files.append(os.path.join(root, file))
                elif "onlines" in file:
                    online_files.append(os.path.join(root, file))
                elif "sbp" in file:
                    sbp_files.append(os.path.join(root, file))

    if realisation_files:
        process_files(realisation_files, ['inn', 'onlyinvoice', 'price', 'quantity', 'company_uuid'], store_uuid_mapping, output_dir)
    if cardcash_files:
        process_files(cardcash_files, ['id', 'company_uuid'], store_uuid_mapping, output_dir)
    if online_files:
        process_files(online_files, ['id', 'company_uuid'], store_uuid_mapping, output_dir)
    if sbp_files:
        process_files(sbp_files, ['id', 'company_uuid'], store_uuid_mapping, output_dir)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python make_readable.py <temp_dir> <output_dir>")
        sys.exit(1)

    temp_dir = sys.argv[1]
    output_dir = sys.argv[2]

    # Store UUID mapping
    store_uuid_mapping = {
        "f966000c-3c48-11dd-96d9-000c6e46fcad": "UN",
        "823cd454-cab4-11eb-a20a-00155dc42e00": "KN",
        "e884414e-345f-11e2-9222-f23cea8074d9": "MC",
        "608fadf8-9055-11e2-ba2e-f1630d599bdb": "BS",
        "53cfe7d1-3b3d-11ee-a22a-00155d59dd05": "MP",
        "800c19a5-3b3e-11ee-a22a-00155d59dd0": "RG",
        "720b6201-a0c4-11e1-9f3c-001e37ed2a0b": "online",
    }

    process_all_excel_files(temp_dir, store_uuid_mapping, output_dir)
