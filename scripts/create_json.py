def create_json_from_excel(output_dir, filename):
    combined_df = pd.read_excel(os.path.join(output_dir, filename))
    
    combined_df['date'] = combined_df['date'].astype(str)
    combined_df['sum'] = combined_df['sum'].astype(float)
    
    json_data = {"payments": combined_df.to_dict(orient='records')}
    
    json_output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.json")
    with open(json_output_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)
    
    print(f"JSON file saved successfully to {json_output_path}")