   import json

   def clean_and_standardize_data(input_file, output_file):
       """
       Cleans and standardizes data from the input JSON file and saves it to the output JSON file.
       """
       with open(input_file, 'r') as file:
           data = json.load(file)

       unique_entries = {}
       for entry in data:
           key = (entry['Name'], entry['Country'], entry['Hall_Stand'], entry['Description'])
           if key not in unique_entries:
               unique_entries[key] = entry

       cleaned_data = list(unique_entries.values())

       for idx, entry in enumerate(cleaned_data, start=1):
           entry['ID'] = idx

       standardized_data = []
       for item in cleaned_data:
           standardized_item = {
               "Name": item.get("Name", "").strip(),
               "Stand_Number": item.get("Stand_Number", "").strip(),
               "Address": {
                   "Line_1": item.get("Address_Line_1", "").strip(),
                   "Line_2": item.get("Address_Line_2", "").strip(),
                   "Line_3": item.get("Address_Line_3", "").strip(),
                   "Line_4": item.get("Address_Line_4", "").strip(),
                   "Postal_Code": item.get("Postal_Code", "").strip(),
                   "Country": item.get("Country", "United Kingdom").strip()
               },
               "Phone_Number": "",  # Removed sensitive information
               "Email_Address": "",  # Removed sensitive information
               "Websites": [
                   item.get("Website_1", "").strip(),
                   item.get("Website_2", "").strip(),
                   item.get("Website_3", "").strip()
               ],
               "Information": item.get("Information", "").replace("Information\n", "").strip(),
               "Product_Categories": [
                   category.strip() for category in item.get("Product Categories", "").splitlines() if category.strip()
               ],
               "Brand_Names": [
                   brand.strip() for brand in item.get("Brand Names", "").splitlines() if brand.strip()
               ],
               "ID": item.get("ID", "")
           }
           standardized_data.append(standardized_item)

       with open(output_file, 'w') as file:
           json.dump(standardized_data, file, indent=4)

       print(f"Cleaned and standardized data saved to {output_file}")

   if __name__ == "__main__":
       clean_and_standardize_data('third_site_output.json', 'cleaned_and_standardized_output.json')