import gspread
from google.oauth2.service_account import Credentials
import asyncio

#==logger settings==
import logging
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
# Вимикаємо DEBUG від google auth
logging.getLogger("google").setLevel(logging.WARNING)

#===================
#temp
ROW_COUNTER = 1;

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("googleapi/gcp_key.json", scopes=scopes)
sheet_id = "1gxcOsmZcY2xBEWzQYvl9wngf4XXO80p74RAxIFocits"
client = gspread.authorize(creds)
mainSheet = client.open_by_key(sheet_id)
valuesNamesList = mainSheet.sheet1.row_values(1)

async def loadGoogleData(self, numberOfRows):
    print('[ARDUINO PROJECT] Loading data...')

    if (numberOfRows == 0):
        numberOfRows = 2


    rowEnd = numberOfRows
    rowStart = 2;

    dataToAdd = []
    for i in range (rowStart, rowEnd+2):
        # valuesList = mainSheet.sheet1.row_values(i)
        valuesList = mainSheet.sheet1.get("A"+str(i)+":D"+str(i))
        # print('[ARDUINO PROJECT] ' + str(valuesList))
        dataToAdd.append(valuesList[0])

    print('[ARDUINO PROJECT] Data to add:\n' + str(dataToAdd))

    for listInside in dataToAdd:
        # listInside.insert(0, str(ROW_COUNTER))
        # listInside.insert(0, str(111))
        self.data_tables.add_row(listInside)
        # ROW_COUNTER += 1


