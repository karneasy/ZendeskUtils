import os
import json
import csv

# Define file paths
json_file_path = "./output/macros_usage.json"  # Path to your JSON file
output_csv_path = "./output/macros_usage.csv"  # Path to save the CSV file

def process_json_and_save_to_csv(json_file, csv_file):
    # Read JSON data
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Open CSV file for writing
    with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Write the header
        writer.writerow(["id", "raw_title", "usage_1h", "usage_24h", "usage_7d", "usage_30d", "dependent_team_values"])

        # Loop through JSON data and write rows
        for page in data:
            macros = page.get("macros", [])
            for macro in macros:
                # Collect dependent_team_* values from actions
                dependent_team_values = []
                actions = macro.get("actions", [])
                for action in actions:
                    if "dependent_team_" in action.get("field", ""):
                        dependent_team_values.append(action.get("value"))

                # Combine dependent_team values into a comma-separated string
                dependent_team_values_str = ", ".join(dependent_team_values)

                try:
                    writer.writerow([
                        macro["id"],
                        macro["raw_title"],
                        macro.get("usage_1h", 0),
                        macro.get("usage_24h", 0),
                        macro.get("usage_7d", 0),
                        macro.get("usage_30d", 0),
                        dependent_team_values_str  # Write extracted dependent_team values
                    ])
                except UnicodeEncodeError as e:
                    print(f"Encoding error for macro ID {macro['id']}: {e}. Skipping this entry.")

    print(f"Data successfully saved to {csv_file}")

# Run the script
process_json_and_save_to_csv(json_file_path, output_csv_path)
