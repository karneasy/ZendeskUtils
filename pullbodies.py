import os
import json
import csv
from settings import DATA_SAVE_PATH

def pull_comment_values():
    # Load the macros.json file
    macros_path = os.path.join(DATA_SAVE_PATH, 'macros.json')
    with open(macros_path, 'r', encoding='utf-8') as json_file:
        macros = json.load(json_file)  # Directly loads a list of macros

    # Open (or create) the CSV file where the results will be saved
    csv_path = os.path.join(DATA_SAVE_PATH, 'bodies.csv')
    with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Macro ID', 'Macro Title', 'Type', 'Value'])

        # Iterate through each macro in the list
        for macro in macros:
            for action in macro['actions']:
                # Check for comment_value and write immediately
                if action['field'] == 'comment_value':
                    writer.writerow([macro['id'], macro['title'], 'comment_value', action['value']])
                # Process side_conversation differently
                elif action['field'] == 'side_conversation':
                    # Split the value into title and body
                    title, body = action['value'].split('","')
                    title = title.strip('"')  # Remove any surrounding quotes
                    body = body.strip('"')
                    # Write two separate rows for title and body
                    writer.writerow([macro['id'], macro['title'], 'sc_title', title])
                    writer.writerow([macro['id'], macro['title'], 'sc_body', body])

    print("Output generated and saved to 'bodies.csv'.")

# Execute the function
pull_comment_values()
