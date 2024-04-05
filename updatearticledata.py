import pandas as pd
import requests
import time
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, DATA_FETCH_PATH

def update_articles_from_csv(csv_path):
    df = pd.read_csv(csv_path)

    # Setup for Zendesk API requests
    auth = requests.auth.HTTPBasicAuth(f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
    headers = {
        'Content-Type': 'application/json'
    }

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        article_id = row['article_id']
        label_names = row['related_to'].split(", ")
        content_tag_ids = row['ct_ids'].split(", ")
        
        # Construct the request payload
        payload = {
            "article": {
                "label_names": label_names,
                "content_tag_ids": content_tag_ids
            }
        }

        # Construct the request URL
        url = f"https://{ZENDESK_URL}.zendesk.com/api/v2/help_center/articles/{article_id}.json"
        
        # Make the PUT request
        print(f"Updating article at URL: {url}")
        response = requests.put(url, json=payload, auth=auth, headers=headers)
        
        # Print the response
        print(f"Response: {response.status_code}, {response.content}")

        # Respect the Zendesk rate limit - adjust sleep time as needed based on your Zendesk plan
        time.sleep(1)  # Sleep for 1 second between requests to avoid hitting rate limits

if __name__ == "__main__":
    csv_file_path = f"{DATA_FETCH_PATH}/guide_structure.csv"
    update_articles_from_csv(csv_file_path)
