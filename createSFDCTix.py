import csv
import os
import json
from settings import DATA_FETCH_PATH, DATA_SAVE_PATH

# Constants
BATCH_SIZE = 100
CSV_FILE_PATH = os.path.join(DATA_FETCH_PATH, 'tickettoload.csv')

def load_csv_data(file_path):
    """Read CSV data into a list of dictionaries."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def save_json(data, filename):
    """Save data to a JSON file."""
    file_path = os.path.join(DATA_SAVE_PATH, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)
    print(f"Saved data to {file_path}")

def create_zendesk_body(batch):
    """Create the JSON body for the Zendesk API request from the batch data."""
    tickets = []
    for ticket in batch:
        # Assuming 'priority' needs to be set manually or can be inferred from another column
        ticket_data = {
            "comment": {"body": ticket['description']},
            "priority": "normal",  # Set a default priority, adjust as needed
            "subject": ticket['subject']
        }
        # Optional: Set priority based on some condition or another column in the CSV
        # if 'priority' in ticket:
        #     ticket_data['priority'] = ticket['priority']
        tickets.append(ticket_data)
    return {'tickets': tickets}

def process_data_in_batches(data, batch_size):
    """Process and save data in batches."""
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        batch_index = i // batch_size + 1  # Compute batch index for naming
        zendesk_body = create_zendesk_body(batch)
        json_filename = f'sfdc_batch_{batch_index}.json'
        save_json(zendesk_body, json_filename)

if __name__ == "__main__":
    data = load_csv_data(CSV_FILE_PATH)
    process_data_in_batches(data, BATCH_SIZE)
