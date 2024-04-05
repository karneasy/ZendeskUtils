import pandas as pd
import json
import os
from settings import DATA_SAVE_PATH, DATA_FETCH_PATH

# Load content tags from JSON
with open(os.path.join(DATA_SAVE_PATH, 'content_tags.json'), 'r') as json_file:
    content_tags = json.load(json_file)

# Convert list of tags to a dictionary for easier lookup
tag_id_mapping = {tag['name']: tag['id'] for tag in content_tags}

# Read the CSV file
csv_file_path = os.path.join(DATA_FETCH_PATH, 'guide_structure.csv')
df = pd.read_csv(csv_file_path)

# Function to get IDs from tag names
def get_tag_ids(tag_names):
    tag_names_list = tag_names.split(',') if not pd.isnull(tag_names) else []
    tag_ids = [str(tag_id_mapping[tag_name.strip()]) for tag_name in tag_names_list if tag_name.strip() in tag_id_mapping]
    return ','.join(tag_ids)

# Apply the function to each row in the 'content_tags' column
df['ct_ids'] = df['content_tags'].apply(get_tag_ids)

# Save the modified DataFrame back to CSV
df.to_csv(csv_file_path, index=False)

print(f"Updated CSV saved to {csv_file_path}")
