import csv
import json
import os
from settings import DATA_FETCH_PATH, DATA_SAVE_PATH

# Constants
BATCH_SIZE = 40
CSV_FILE_PATH = os.path.join(DATA_FETCH_PATH, 'macrostodesalto.csv')

def load_csv_data(file_path):
    """Read CSV data into a list of dictionaries."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader if "@SALTO" in row['actions']]

def parse_actions(actions):
    """Parse the actions field and return as a dictionary."""
    try:
        # Convert the string in 'actions' to a JSON object
        return json.loads(actions)
    except json.JSONDecodeError:
        return None  # Return None or some error handling if the JSON is invalid

def create_macros_json(batches):
    """Create and save JSON files from batches of macro data."""
    for index, batch in enumerate(batches):
        macros = [{'id': int(macro['id']), 'actions': parse_actions(macro['actions'])} for macro in batch if parse_actions(macro['actions'])]
        json_data = {'macros': macros}
        json_file_path = os.path.join(DATA_SAVE_PATH, f'macros_batch_{index + 1}.json')
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent=2)
        print(f"Saved JSON batch {index + 1} to {json_file_path}")

def batch_data(data, batch_size):
    """Divide data into batches."""
    return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

if __name__ == "__main__":
    data = load_csv_data(CSV_FILE_PATH)
    batches = batch_data(data, BATCH_SIZE)
    create_macros_json(batches)
