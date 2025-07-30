from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "/Users/arslansalim/Desktop/formi-voice-backend/data/my-project-formiai-a259e5b4300b.json")
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID", "1M_jCLWEUB27c_UYK8OVdXO5PqdvHWlcGTJdFDAJFR_4")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

def log_conversation(row_data: list):
    try:
        request = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A1',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': [row_data]}
        )
        response = request.execute()
        return response
    except Exception as e:
        raise e
