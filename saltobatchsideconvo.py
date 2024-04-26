import csv
import json
import os
from settings import DATA_FETCH_PATH, DATA_SAVE_PATH

CSV_FILE_PATH = os.path.join(DATA_FETCH_PATH, 'macrostodesalto.csv')
OUTPUT_JSON_PATH = os.path.join(DATA_SAVE_PATH, 'macros_output.json')

def load_csv_data(file_path):
    """Read CSV data and parse it into a list of dictionaries, handling JSON parsing issues."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = []
        for row in reader:
            try:
                # Attempt to parse the JSON in the 'actions' column
                actions = json.loads(row['actions'])
                row['actions'] = actions  # Replace the string with its parsed JSON
                data.append(row)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON for row {row['id']}: {e}")
    return data

def format_to_json(data):
    """Convert data into the specified JSON format for Zendesk macros."""
    macros = [{'id': int(item['id']), 'actions': item['actions']} for item in data]
    return {"macros": macros}

def save_to_json(data, output_path):
    """Save the formatted data to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)
    print(f"Data saved to JSON file at {output_path}")

if __name__ == "__main__":
    # Load data from the CSV, parsing JSON within
    macro_data = load_csv_data(CSV_FILE_PATH)
    # Convert to JSON format
    json_data = format_to_json(macro_data)
    # Save to JSON file
    save_to_json(json_data, OUTPUT_JSON_PATH)
