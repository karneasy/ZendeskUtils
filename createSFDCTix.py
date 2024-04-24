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

def save_batch_as_csv(batch, batch_index):
    """Save each batch of data to a separate CSV file."""
    batch_file_path = os.path.join(DATA_SAVE_PATH, f'batch_{batch_index + 1}.csv')
    fieldnames = ['email', 'subject', 'description', 'created date', 'tags']
    with open(batch_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(batch)
    print(f"Saved batch {batch_index + 1} to '{batch_file_path}'.")

def create_zendesk_body(batch):
    """Create the JSON body for the Zendesk API request from the batch data."""
    tickets = [{'ticket': {'requester': {'email': ticket['email']},
                           'subject': ticket['subject'],
                           'description': ticket['description'],
                           'created_at': ticket['created date'],
                           'tags': ticket['tags'].split()}} for ticket in batch]
    return json.dumps({'tickets': tickets}, indent=2)

def process_data_in_batches(data, batch_size):
    """Process and save data in batches."""
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        save_batch_as_csv(batch, i // batch_size)
        zendesk_body = create_zendesk_body(batch)
        print(f"Batch {i // batch_size + 1} Zendesk body: {zendesk_body}")

if __name__ == "__main__":
    data = load_csv_data(CSV_FILE_PATH)
    process_data_in_batches(data, BATCH_SIZE)
