import pandas as pd
from settings import DATA_FETCH_PATH, DATA_SAVE_PATH

def append_prod_id_to_sbox(prod_file, sbox_file, output_file):
    # Load the CSV files
    prod_df = pd.read_csv(prod_file)
    sbox_df = pd.read_csv(sbox_file)

    # Merge DataFrames on 'name', keeping only columns relevant for the merge and output
    merged_df = pd.merge(sbox_df, prod_df[['id', 'name']], on='name', suffixes=('', '_prod'))

    # Rename the 'id' column from 'prod.csv' to 'prod_id' for clarity
    merged_df.rename(columns={'id_prod': 'prod_id'}, inplace=True)

    # Select columns from sbox_df and append 'prod_id'
    result_df = merged_df[list(sbox_df.columns) + ['prod_id']]

    # Save the resulting DataFrame to a new CSV
    result_df.to_csv(output_file, index=False)

# Construct file paths from settings
prod_path = f"{DATA_FETCH_PATH}/prod.csv"
sbox_path = f"{DATA_FETCH_PATH}/sbox.csv"
output_path = f"{DATA_SAVE_PATH}/merged_output.csv"

# Call the function with your filenames
append_prod_id_to_sbox(prod_path, sbox_path, output_path)
