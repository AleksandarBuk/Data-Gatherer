import json
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_json_format(input_file, output_json_file, output_csv_file, output_xlsx_file):
    """Transforms JSON data and saves it in JSON, CSV, and XLSX formats."""
    try:
        with open(input_file, 'r') as file:
            data = json.load(file)
    except Exception as e:
        logging.error(f"Error reading input file: {e}")
        return

    transformed_data = []
    for item in data:
        company_info_lines = item.get("Company Info", "").splitlines()
        transformed_item = {
            "Name": item.get("Name", ""),
            "Stand_Number": item.get("Stand Number", ""),
            "Address_Line_1": company_info_lines[0] if len(company_info_lines) > 0 else '',
            "Address_Line_2": company_info_lines[1] if len(company_info_lines) > 1 else '',
            "Address_Line_3": company_info_lines[2] if len(company_info_lines) > 2 else '',
            "Address_Line_4": company_info_lines[3] if len(company_info_lines) > 3 else '',
            "Postal_Code": company_info_lines[4] if len(company_info_lines) > 4 else '',
            "Country": company_info_lines[-1] if len(company_info_lines) > 5 else 'Default',  
            "Phone_Number": company_info_lines[5] if len(company_info_lines) > 5 else '',
            "Email_Address": company_info_lines[6] if len(company_info_lines) > 6 else '',
            "Website_1": company_info_lines[7] if len(company_info_lines) > 7 else '',
            "Website_2": company_info_lines[8] if len(company_info_lines) > 8 else '',
            "Website_3": company_info_lines[9] if len(company_info_lines) > 9 else '',
            "Information": item.get("Information", "").replace("Information\n", ""),
        }

        product_categories = item.get("Product Categories", "").splitlines()
        for i in range(1, 5):
            transformed_item[f"Product_Category_{i}"] = product_categories[i] if len(product_categories) > i else ''

        brand_names = item.get("Brand Names", "").splitlines()
        for i in range(1, 5):
            transformed_item[f"Brand_Name_{i}"] = brand_names[i] if len(brand_names) > i else ''

        transformed_item["ID"] = item.get("ID", "")
        transformed_data.append(transformed_item)

    try:
        with open(output_json_file, 'w') as file:
            json.dump(transformed_data, file, indent=4)
    except Exception as e:
        logging.error(f"Error writing output JSON file: {e}")
        return

    try:
        df = pd.DataFrame(transformed_data)
        df.to_csv(output_csv_file, index=False)
        df.to_excel(output_xlsx_file, index=False)
    except Exception as e:
        logging.error(f"Error writing output CSV/XLSX file: {e}")
        return

    logging.info("Transformation completed successfully")

if __name__ == "__main__":
    transform_json_format('second_member_list_data.json', 'transformed_second_member_list_data.json', 'transformed_second_member_list_data.csv', 'transformed_second_member_list_data.xlsx')