import csv
import json
import os
from settings import DATA_SAVE_PATH, DATA_FETCH_PATH  # Ensure DATA_FETCH_PATH is defined in your settings

def load_dynamic_content_items(json_file_path):
    """Load dynamic content items from a JSON file."""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def add_placeholders_to_csv(json_data, csv_file_path, output_csv_path):
    """
    Add placeholders to the CSV based on dynamic content titles.
    
    Args:
        json_data: The list of dynamic content items loaded from JSON.
        csv_file_path: The path to the input CSV file located in DATA_FETCH_PATH.
        output_csv_path: The path where the output CSV will be saved in DATA_SAVE_PATH.
    """
    # Prepare a mapping of DC titles to placeholders for quick lookup
    dc_title_to_placeholder = {item['name']: item.get('placeholder', '') for item in json_data}

    with open(csv_file_path, mode='r', encoding='utf-8') as infile, \
         open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['dc_placeholder']  # Add new column
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in reader:
            # Check if the DC title from the CSV exists in the JSON mapping
            dc_title = row['dc_title']
            placeholder = dc_title_to_placeholder.get(dc_title, '')  # Default to empty string if not found
            row['dc_placeholder'] = placeholder
            writer.writerow(row)

if __name__ == "__main__":
    json_file_path = os.path.join(DATA_SAVE_PATH, 'dcitems.json')
    csv_file_path = os.path.join(DATA_FETCH_PATH, 'macrostomake.csv')
    output_csv_path = os.path.join(DATA_SAVE_PATH, 'macrostomake_with_placeholders.csv')

    # Load dynamic content items from JSON
    dc_items = load_dynamic_content_items(json_file_path)

    # Process the CSV to add placeholders
    add_placeholders_to_csv(dc_items, csv_file_path, output_csv_path)

    print("Completed adding placeholders to the CSV.")
