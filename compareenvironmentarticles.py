import pandas as pd
from settings import DATA_FETCH_PATH, DATA_SAVE_PATH

def compare_and_extract(prod_file, sbox_file, output_file):
    # Load the CSV files
    prod_df = pd.read_csv(prod_file)
    sbox_df = pd.read_csv(sbox_file)

    # Identify matching columns based on column names
    common_columns = prod_df.columns.intersection(sbox_df.columns)

    # Initialize a DataFrame for the results
    result_df = pd.DataFrame(columns=['ID', 'body', 'label_names'])

    # Loop through the common columns to find differences
    for column in common_columns:
        if column in ['body', 'label_names']:  # Check only specific columns if needed
            # Compare the columns
            differences = prod_df[column] != sbox_df[column]
            if differences.any():
                # Extract differing rows and specific columns
                differing_rows = prod_df[differences]
                new_rows = differing_rows[['ID', 'body', 'label_names']]
                result_df = pd.concat([result_df, new_rows], ignore_index=True)

    # Save the resulting DataFrame to a new CSV
    result_df.drop_duplicates(inplace=True)
    result_df.to_csv(output_file, index=False)

# Construct file paths from settings
prod_path = f"{DATA_FETCH_PATH}/prod.csv"
sbox_path = f"{DATA_FETCH_PATH}/sbox.csv"
output_path = f"{DATA_SAVE_PATH}/differences.csv"

# Call the function with your filenames
compare_and_extract(prod_path, sbox_path, output_path)
