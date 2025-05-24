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

async def loadGoogleData(self, numberOfRows, rowStart):
    print('[ARDUINO PROJECT] Loading data from rowStart: ' + str(rowStart))

    if (numberOfRows == 0):
        numberOfRows = 2

    totalRows = len(mainSheet.sheet1.col_values(1))

    rowEnd = totalRows
    rowStart = rowStart + max(3, rowEnd - numberOfRows + 1)  # не вище рядка 3

    dataToAdd = []
    for i in range(rowEnd, rowStart - 1, -1):  # проходимо знизу вгору
        valuesList = mainSheet.sheet1.get(f"A{i}:D{i}")
        if valuesList:
            dataToAdd.append(valuesList[0])

    print('[ARDUINO PROJECT] Data to add: ' + str(len(dataToAdd)))

    for listInside in dataToAdd:
        listInside[1] = str(int(float(listInside[1]))) + '%'
        self.mainTable.add_row(listInside)
