import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet_data():
    try:
        #Define scope
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

        #Load credentials
        creds = ServiceAccountCredentials.from_json_keyfile_name('apd.json', scope)
        client = gspread.authorize(creds)

        #Open the Google Sheet
        sheet = client.open("test_data").sheet1

        #Get all records
        data = sheet.get_all_records()
        return data

    except Exception as e:
        print("Error fetching data:", e)
        return []


import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_coordinates():
    try:
        #Google Sheets API setup
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive.file',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('apd.json', scope)
        client = gspread.authorize(creds)

        #Open the sheet and fetch coordinates from cell A1
        sheet = client.open('test_data').sheet1
        coordinates = sheet.acell('F2').value + ',' + sheet.acell('F3').value
        print(coordinates)
        return coordinates
    except Exception as e:
        print(f"Error retrieving coordinates: {e}")
        return None