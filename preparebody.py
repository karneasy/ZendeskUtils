import os
import json
from settings import DATA_SAVE_PATH

def replace_string_in_actions(data, search_string, replacement_string):
    for entry in data:
        for action in entry.get("actions", []):
            if isinstance(action.get("value"), list):
                for i, value in enumerate(action.get("value")):
                    if search_string in value:
                        action["value"][i] = value.replace(search_string, replacement_string)

def main():
    search_string = "Ticket {{ticket.id}} Transferred from Zendesk"
    replacement_string = "{{ticket.title}}"

    macros_file_path = os.path.join(DATA_SAVE_PATH, "macros.json")
    with open(macros_file_path, "r") as file:
        data = json.load(file)

    replace_string_in_actions(data, search_string, replacement_string)

    updated_macros_file_path = os.path.join(DATA_SAVE_PATH, "updated_macros.json")
    with open(updated_macros_file_path, "w") as outfile:
        json.dump(data, outfile, indent=4)

    print("String replaced and saved to updated_macros.json")

if __name__ == "__main__":
    main()
