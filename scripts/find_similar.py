import json
import pandas as pd
from dotenv import load_dotenv
import os

def load_json(file_path):
    """
    Load data from a JSON file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def load_excel(file_path):
    """
    Load data from an Excel file.
    """
    return pd.read_excel(file_path).to_dict(orient='records')

def compare_json_excel(json_file, excel_file):
    """
    Compare data from JSON and Excel files and find similar names.
    """
    json_data = load_json(json_file)
    excel_data = load_excel(excel_file)

    name_to_id_json = {item['Name'].lower(): item['ID'] for item in json_data if 'Name' in item and 'ID' in item}
    name_to_id_excel = {item['Name'].lower(): item['ID'] for item in excel_data if 'Name' in item and 'ID' in item}

    similar_names = set(name_to_id_json.keys()).intersection(name_to_id_excel.keys())
    similar_ids = [(name_to_id_json[name], name_to_id_excel[name]) for name in similar_names]

    similar_data = [{'Name': name, 'JSON_ID': name_to_id_json[name], 'Excel_ID': name_to_id_excel[name]} for name in similar_names]
    df = pd.DataFrame(similar_data)
    df.to_excel('same_from_each_site.xlsx', index=False)

    return similar_ids

json_file = 'first_member_list_data.json'
excel_file = 'second_member_list_data.xlsx'

similar_ids = compare_json_excel(json_file, excel_file)
print(f"IDs of similar names: {similar_ids}")