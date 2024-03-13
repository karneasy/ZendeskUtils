from dotenv import load_dotenv
import os

load_dotenv('variables.env')  # Load environment variables from .env file

ZENDESK_URL = os.getenv("ZENDESK_URL")
ZENDESK_EMAIL = os.getenv("ZENDESK_EMAIL")
ZENDESK_TOKEN = os.getenv("ZENDESK_TOKEN")
DATA_SAVE_PATH = os.getenv("DATA_SAVE_PATH", "default/path")
DATA_FETCH_PATH = os.getenv("DATA_FETCH_PATH", "default/path")

#These are your endpoints that my json function will call, if it uses the normal zendesk cursor pagination, just add another line and itll get those too.
#Added the name of the response for the data extraction
ZENDESK_API_ENDPOINTS = {
    "/api/v2/users": "users"
}