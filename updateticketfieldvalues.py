import csv
import json
from zenpy import Zenpy
from zenpy.lib.api_objects import CustomFieldOption
from settings import ZENDESK_EMAIL, ZENDESK_TOKEN, ZENDESK_URL, DATA_FETCH_PATH, DATA_SAVE_PATH

# Function to read CSV and return a list of JSON objects
def read_csv_and_generate_json(csv_path):
    json_objects = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Assuming 'value', 'tag', and 'default' are column names in your CSV
            json_object = {
                "custom_field_option": {
                    "id": int(row['value']),  # Update this as needed
                    "name": row['tag'],
                    "default": row['default'] == 'True'
                }
            }
            json_objects.append(json_object)
    return json_objects

# Function to use Zenpy to do something with the JSON objects
# You will need to replace this with the actual code to create or update in Zendesk
def process_json_objects_with_zenpy(json_objects):
    # Setup Zenpy client (fill in your actual credentials)
    creds = {
        'email': ZENDESK_EMAIL,
        'token': ZENDESK_TOKEN,
        'subdomain': ZENDESK_URL
    }
    zenpy_client = Zenpy(**creds)

    for obj in json_objects:
        # Here you should replace this print statement with the actual Zenpy operation
        # For example, creating or updating a custom field option in Zendesk
        print(json.dumps(obj, indent=4))
        # Example placeholder operation
        # custom_field_option = CustomFieldOption(**obj['custom_field_option'])
        # zenpy_client.ticket_fields.update(custom_field_option)

if __name__ == "__main__":
    csv_path = getattr(settings, 'DATA_FETCH_PATH', '')
    json_objects = read_csv_and_generate_json(csv_path)
    process_json_objects_with_zenpy(json_objects)
