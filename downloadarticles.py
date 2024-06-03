import json
from zenpy import Zenpy
import settings

# Initialize Zenpy client using settings from settings.py
creds = {
    'email': settings.ZENDESK_EMAIL,
    'token': settings.ZENDESK_TOKEN,
    'subdomain': settings.ZENDESK_URL
}

zenpy_client = Zenpy(**creds)

# Function to get all articles
def get_all_articles():
    articles = []
    # Get articles in batches
    for article in zenpy_client.help_center.articles():
        articles.append({
            'id': article.id,
            'title': article.title,
            'body': article.body,
            'author_id': article.author_id,
            'created_at': article.created_at,
            'updated_at': article.updated_at,
            'section_id': article.section_id,
            'tags': article.label_names,  # tags are stored in label_names
            'content_tag_ids': article.content_tag_ids
        })
    return articles

# Fetch all articles
all_articles = get_all_articles()

# Save articles to a JSON file
with open(settings.DATA_SAVE_PATH, 'w') as file:
    json.dump(all_articles, file, indent=4)

print(f"Saved {len(all_articles)} articles to {settings.DATA_SAVE_PATH}")
