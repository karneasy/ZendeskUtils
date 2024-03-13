import os
import requests
from requests.auth import HTTPBasicAuth
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, DATA_SAVE_PATH

def post_memberships_and_save_response():
    # Find all 'memberstoadd_*.json' files in the DATA_SAVE_PATH
    memberstoadd_files = [file for file in os.listdir(DATA_SAVE_PATH) if file.startswith('memberstoadd_') and file.endswith('.json')]
    
    # Prepare authentication for Zendesk API
    auth = HTTPBasicAuth(f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Iterate over each file to make API call
    for file_name in memberstoadd_files:
        file_path = os.path.join(DATA_SAVE_PATH, file_name)
        with open(file_path, 'r') as file:
            # Use the file content as the request body
            data = file.read()
            
        # Define the API endpoint for creating organization memberships in bulk
        url = f"{ZENDESK_URL}/api/v2/organization_memberships/create_many.json"
        
        # Make the POST request
        response = requests.post(url, headers=headers, auth=auth, data=data)
        
        # Log the status code or response for debugging
        print(f"Response for {file_name}: Status Code {response.status_code}")
        
        # Save the response to a text file with the same name as the batch, but with .txt extension
        response_file_name = os.path.splitext(file_name)[0] + '.txt'
        response_file_path = os.path.join(DATA_SAVE_PATH, response_file_name)
        with open(response_file_path, 'w') as response_file:
            response_file.write(response.text)
        
        print(f"Response saved to {response_file_path}")

# Call the function to process the files and make API calls
if __name__ == "__main__":
    post_memberships_and_save_response()
