#!/usr/bin/env python
# -*- coding: utf8 -*-
import signal
import gspread
from oauth2client.service_account import ServiceAccountCredentials
def __init__(team, runde, orderedValues):
    
    print("ENTER WRITE ORDERS!") 
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    
    # opening necessary sheet
    team_sheet = client.open("Seminar").worksheet("Team"+str(team))
   
    #Write ordered amounts to spreadsheet
    rangeStart = gspread.utils.rowcol_to_a1(3, runde+1)
    rangeEnd = gspread.utils.rowcol_to_a1(6, runde+1)
    rangeString = rangeStart + ":" + rangeEnd
    orderCells = team_sheet.range(rangeString)
    print len(orderCells)
    print len(orderedValues)
    for i in range(0, len(orderCells)):
        orderCells[i].value = orderedValues[i]
    team_sheet.update_cells(orderCells)
    return