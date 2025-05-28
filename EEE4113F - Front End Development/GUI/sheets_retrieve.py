import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if getattr(sys, 'frozen', False):  # Running as compiled
        base_path = sys._MEIPASS
    else:  # Running in development
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def get_sheet_data():
    try:
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]

        # Use get_resource_path to get JSON file
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            get_resource_path('apd_new.json'),
            scope
        )

        client = gspread.authorize(creds)
        sheet = client.open("test_data").sheet1
        return sheet.get_all_records()

    except Exception as e:
        print("Error fetching data:", e)
        return []


def get_coordinates():
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive.file',
                 'https://www.googleapis.com/auth/drive']


        creds = ServiceAccountCredentials.from_json_keyfile_name(
            get_resource_path('apd_new.json'),
            scope
        )

        client = gspread.authorize(creds)
        sheet = client.open('test_data').sheet1
        coordinates = sheet.acell('G2').value + ',' + sheet.acell('G3').value
        return coordinates

    except Exception as e:
        print(f"Error retrieving coordinates: {e}")
        return None