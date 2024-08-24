import pandas as pd
import json

def convert_json_to_xlsx_and_csv(json_file, xlsx_file, csv_file):
    """
    Convert JSON file to both Excel and CSV files.
    """
    with open(json_file, 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    df.to_excel(xlsx_file, index=False)
    print(f"Converted JSON to {xlsx_file}")

    df.to_csv(csv_file, index=False)
    print(f"Converted JSON to {csv_file}")

convert_json_to_xlsx_and_csv('first_member_list_data.json', 'first_member_list.xlsx', 'first_member_list.csv')

convert_json_to_xlsx_and_csv('second_member_list_data.json', 'second_member_list_data.xlsx', 'second_member_list_data.csv')