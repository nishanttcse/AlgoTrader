import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

def connect_to_sheet(sheet_name, credentials_file):
    try:
        creds = Credentials.from_service_account_file(credentials_file, scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ])
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name)
        return sheet
    except gspread.SpreadsheetNotFound:
        raise Exception(f"Spreadsheet '{sheet_name}' not found. Make sure it exists and you're authorized.")
    except Exception as e:
        raise Exception(f"Error connecting to sheet: {e}")

def log_dataframe(sheet, df, worksheet_title):
    try:
        # Remove MultiIndex if any
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(filter(None, col)).strip() for col in df.columns.values]

        values = [df.columns.tolist()] + df.fillna("").astype(str).values.tolist()

        try:
            worksheet = sheet.worksheet(worksheet_title)
            worksheet.clear()
        except gspread.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title=worksheet_title, rows="100", cols="20")

        worksheet.update(values)
        print(f"✅ Data logged to Google Sheet: {worksheet_title}")
    
    except Exception as e:
        print(f"❌ Failed to log data to worksheet '{worksheet_title}': {e}")
