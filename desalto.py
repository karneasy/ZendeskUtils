import csv
import os
from settings import DATA_FETCH_PATH, DATA_SAVE_PATH

CSV_FILE_PATH = os.path.join(DATA_FETCH_PATH, 'macrostodesalto.csv')
OUTPUT_CSV_FILE_PATH = os.path.join(DATA_SAVE_PATH, 'filtered_macros.csv')

def load_and_filter_data(file_path):
    """Read and filter CSV data, printing IDs and saving required entries."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        filtered_data = [row for row in reader if "@SALTO" in row['actions']]
        
    return filtered_data

def print_ids(data):
    """Print the ID of each entry that contains '@SALTO'."""
    for row in data:
        print(f"ID: {row['id']}")

def save_filtered_data(data, output_file_path):
    """Save the filtered data to a new CSV file with only ID and actions columns."""
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'actions'])
        writer.writeheader()
        writer.writerows(data)
    print(f"Filtered data has been saved to {output_file_path}")

if __name__ == "__main__":
    data = load_and_filter_data(CSV_FILE_PATH)
    print_ids(data)
    save_filtered_data(data, OUTPUT_CSV_FILE_PATH)
