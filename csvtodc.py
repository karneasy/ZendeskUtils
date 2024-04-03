import os
import csv
from zenpy import Zenpy
from zenpy.lib.api_objects import Item
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, DATA_SAVE_PATH

# Set up Zenpy with your Zendesk credentials
zenpy_client = Zenpy(subdomain=ZENDESK_URL, email=ZENDESK_EMAIL, token=ZENDESK_TOKEN)

def create_dynamic_content_items(csv_file_path):
    """
    Reads a CSV file and creates dynamic content items in Zendesk for each row.
    Each item will have a default locale and additional variants for the specified locale IDs.
    """
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dc_title = row['dc_title']
            dc_body = row['dc_body']

            # Prepare the variants
            variants = [
                {'locale_id': 10, 'content': dc_body},   # Variant for default locale
                {'locale_id': 1176, 'content': dc_body}  # Additional variant for locale ID 1176
            ]

            # Create the dynamic content item with a default locale
            item = Item(
                name=dc_title,
                default_locale_id=10,  # Default locale ID
                variants=variants
            )

            # Attempt to create the dynamic content item in Zendesk
            try:
                created_item = zenpy_client.dynamic_content_items.create(item)
                print(f"Successfully created dynamic content item: {created_item.id}")
            except Exception as e:
                print(f"Failed to create dynamic content item for '{dc_title}'. Error: {e}")

if __name__ == "__main__":
    # Define the path to your CSV file
    csv_file_path = os.path.join(DATA_SAVE_PATH, 'dynamic_content.csv')
    # Call the function to create dynamic content items
    create_dynamic_content_items(csv_file_path)
