import pandas as pd
from settings import DATA_FETCH_PATH, DATA_SAVE_PATH

def compare_and_extract(prod_file, sbox_file, output_file):
    # Load the CSV files
    prod_df = pd.read_csv(prod_file)
    sbox_df = pd.read_csv(sbox_file)

    # Merge DataFrames on 'name' to align rows for comparison
    merged_df = pd.merge(sbox_df, prod_df, on='name', suffixes=('_sbox', '_prod'))

    # Filter out rows where 'body' in both DataFrames is the same
    differing_rows = merged_df[merged_df['body_sbox'] != merged_df['body_prod']]

    # Create a new DataFrame with the desired columns
    result_df = pd.DataFrame({
        'id': differing_rows['id_sbox'],
        'name': differing_rows['name'],
        'label_names': differing_rows['label_names_prod'],
        'body': differing_rows['body_prod']
    })

    # Save the resulting DataFrame to a new CSV
    result_df.to_csv(output_file, index=False)

# Construct file paths from settings
prod_path = f"{DATA_FETCH_PATH}/prod.csv"
sbox_path = f"{DATA_FETCH_PATH}/sbox.csv"
output_path = f"{DATA_SAVE_PATH}/diff_output.csv"

# Call the function with your filenames
compare_and_extract(prod_path, sbox_path, output_path)
