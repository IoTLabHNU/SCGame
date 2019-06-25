#!/usr/bin/python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def init():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    uid = [123,456,789,11]
    # opening necessary sheets
    master_sheet = client.open("Seminar").sheet1        
    team_uid_cell = master_sheet.find(str(uid[0])+str(uid[1])+str(uid[2])+ str(uid[3]))
    team = master_sheet.cell(team_uid_cell.row, team_uid_cell.col-1).value
    print(team)
    return (team,True)
    


