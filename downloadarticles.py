import requests
import csv
import settings

# Endpoint URL
url = f"https://{settings.ZENDESK_URL}.zendesk.com/api/v2/help_center/articles.json"

# Authentication
auth = (f"{settings.ZENDESK_EMAIL}/token", settings.ZENDESK_TOKEN)

# Function to get all articles
def get_all_articles():
    articles = []
    current_url = url
    page = 1
    while current_url:
        print(f"Fetching page {page}...")
        response = requests.get(current_url, auth=auth)
        response.raise_for_status()  # Check for request errors
        data = response.json()
        articles.extend(data['articles'])
        current_url = data['next_page']  # Get the next page URL
        print(f"Fetched {len(data['articles'])} articles from page {page}")
        page += 1
    print(f"Total articles fetched: {len(articles)}")
    return articles

# Fetch all articles
print("Starting to fetch all articles...")
all_articles = get_all_articles()

# Define the CSV file path
csv_file_path = settings.DATA_SAVE_PATH

# Save articles to a CSV file
print(f"Saving articles to {csv_file_path}...")
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['id', 'title', 'body', 'author_id', 'created_at', 'updated_at', 'section_id', 'tags', 'content_tag_ids'])
    # Write the article data
    for article in all_articles:
        writer.writerow([
            article['id'],
            article['title'],
            article['body'],
            article['author_id'],
            article['created_at'],
            article['updated_at'],
            article['section_id'],
            ','.join(article['label_names']),  # Convert tags list to a comma-separated string
            ','.join(map(str, article.get('content_tag_ids', [])))  # Convert content_tag_ids list to a comma-separated string
        ])
print(f"Articles saved successfully to {csv_file_path}")
