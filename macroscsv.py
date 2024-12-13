import os
import json
import csv

# Define file paths
json_file_path = "./output/macros_usage.json"  # Path to your JSON file
output_csv_path = "./output/macros_usage.csv"  # Path to save the CSV file

def process_json_and_save_to_csv(json_file, csv_file):
    # Read JSON data
    with open(json_file, "r") as file:
        data = json.load(file)

    # Open CSV file for writing
    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write the header
        writer.writerow(["id", "raw_title", "usage_1h", "usage_24h", "usage_7d", "usage_30d"])

        # Loop through JSON data and write rows
        for page in data:
            macros = page.get("macros", [])
            for macro in macros:
                writer.writerow([
                    macro["id"],
                    macro["raw_title"],
                    macro.get("usage_1h", 0),
                    macro.get("usage_24h", 0),
                    macro.get("usage_7d", 0),
                    macro.get("usage_30d", 0)
                ])

    print(f"Data successfully saved to {csv_file}")

# Run the script
process_json_and_save_to_csv(json_file_path, output_csv_path)
