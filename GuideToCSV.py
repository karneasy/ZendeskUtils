import json
import csv
from settings import DATA_SAVE_PATH

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def find_parent_sections(sections):
    parent_sections = {}
    for section in sections:
        parent_id = section.get('parent_section_id')
        if parent_id is None:
            parent_sections[section['id']] = {'name': section['name'], 'articles': []}
        else:
            if parent_id not in parent_sections:
                parent_sections[parent_id] = {'name': '', 'articles': []}
            parent_sections[parent_id]['articles'].append(section)
    return parent_sections

def process_articles(articles, sections):
    section_mapping = {section['id']: section['name'] for section in sections}
    for article in articles:
        section_id = article['section_id']
        if section_id in section_mapping:
            article['section_name'] = section_mapping[section_id]
        else:
            article['section_name'] = 'Unknown'

def write_to_csv(parent_sections, articles, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Article ID', 'Article Title'] + list(parent_sections.values())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for article in articles:
            row = {'Article ID': article['id'], 'Article Title': article['title']}
            section_name = article['section_name']
            for parent_id, parent_section in parent_sections.items():
                if section_name == parent_section['name']:
                    row[section_name] = 'X'
                else:
                    row[parent_section['name']] = ''
            writer.writerow(row)

def main():
    categories_data = load_json('categories.json')
    articles_data = load_json('articles.json')
    
    parent_sections = find_parent_sections(categories_data['sections'])
    process_articles(articles_data['articles'], categories_data['sections'])
    
    write_to_csv(parent_sections, articles_data['articles'], DATA_SAVE_PATH)

if __name__ == "__main__":
    main()
