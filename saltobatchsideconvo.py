import csv
import json
import os
from settings import DATA_FETCH_PATH, DATA_SAVE_PATH, ZENDESK_EMAIL, ZENDESK_TOKEN, ZENDESK_URL

# Path to the CSV file with macro data
CSV_FILE_PATH = os.path.join(DATA_FETCH_PATH, 'macrostodesalto.csv')
# Path to save the JSON output
OUTPUT_JSON_PATH = os.path.join(DATA_SAVE_PATH, 'macros_output.json')

def load_csv_data(file_path):
    """Read CSV data and parse it into a list of dictionaries."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def format_to_json(data):
    """Convert data from the CSV into the specified JSON format for Zendesk macros."""
    macros = []
    for item in data:
        # Assuming the actions column contains a string that needs to be converted into a JSON format
        actions_list = json.loads(item['actions'])  # Parse the JSON string from the CSV
        macro = {
            "id": int(item['id']),
            "actions": actions_list
        }
        macros.append(macro)

    return {"macros": macros}

def save_to_json(data, output_path):
    """Save the formatted data to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)
    print(f"Data saved to JSON file at {output_path}")

if __name__ == "__main__":
    # Load data from the CSV
    macro_data = load_csv_data(CSV_FILE_PATH)
    # Convert to JSON format
    json_data = format_to_json(macro_data)
    # Save to JSON file
    save_to_json(json_data, OUTPUT_JSON_PATH)
