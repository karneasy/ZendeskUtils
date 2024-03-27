import csv
from zenpy import Zenpy
from zenpy.lib.api_objects import Item
from settings import ZENDESK_EMAIL, ZENDESK_TOKEN, ZENDESK_URL, DATA_FETCH_PATH

creds = {
    'email': ZENDESK_EMAIL,
    'token': ZENDESK_TOKEN,
    'subdomain': ZENDESK_URL
}

zenpy_client = Zenpy(**creds)

csv_file = DATA_FETCH_PATH + '/macrosintodc.csv'

with open(csv_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:

        item = Item(
            name=row['title'],
            content=row['text'],
            default_locale_id=1176
        )
        
        try:
            created_item = zenpy_client.dynamic_content.create(item)
            print(f'Successfully created dynamic content item: {row["title"]}')
        except Exception as e:
            print(f'Failed to create dynamic content item: {row["title"]}. Error: {str(e)}')
