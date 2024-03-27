import csv
import json
from zenpy import Zenpy
from zenpy.lib.api_objects import TicketField, CustomFieldOption
from settings import ZENDESK_EMAIL, ZENDESK_TOKEN, ZENDESK_URL, DATA_FETCH_PATH

def read_csv_and_generate_json(csv_path):
    json_objects = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            json_object = {
                "value": row['value'],
                "name": row['tag'],
                "default": row['default'] == 'True'
            }
            json_objects.append(json_object)
    return json_objects

def process_json_objects_with_zenpy(json_objects, field_id):
    creds = {
        'email': ZENDESK_EMAIL,
        'token': ZENDESK_TOKEN,
        'subdomain': ZENDESK_URL.split('//')[1]  # Assuming ZENDESK_URL is in the format http(s)://your_subdomain.zendesk.com
    }
    zenpy_client = Zenpy(**creds)

    ticket_field = zenpy_client.ticket_fields(id=field_id)
    if not ticket_field.custom_field_options:
        ticket_field.custom_field_options = []

    for obj in json_objects:
        # Assuming you want to add or update custom field options
        custom_field_option = CustomFieldOption(**obj)
        # Update the options list with new or modified options
        # This example just adds the new option; you might need to check if it exists and update it instead
        ticket_field.custom_field_options.append(custom_field_option)

    # Update the ticket field with new custom field options
    # Note: This is a simplistic approach; you may need to adjust it based on your exact requirements
    zenpy_client.ticket_fields.update(ticket_field)

if __name__ == "__main__":
    csv_path = DATA_FETCH_PATH + 'dependent.csv'  # Adjusted to concatenate the filename
    json_objects = read_csv_and_generate_json(csv_path)
    process_json_objects_with_zenpy(json_objects, 12345)
