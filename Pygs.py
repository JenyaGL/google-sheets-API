# Libs

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
import random
import pandas as pd


# ------------------------------
current_dir = os.path.dirname(os.path.realpath(__file__))
key_file = os.path.join(current_dir, 'configurations', 'red-function-478012-q6-56f3b2178e8c.json')

scopes = ['https://www.googleapis.com/auth/drive']

# this is the spreadsheet id we will work with
spreadsheet_id = '1UUtUT06eVcxj4CfMGHdZKJWxIcIyYZINXJzid8J_wO4'

# credentials
Credentials = Credentials.from_service_account_file(key_file, scopes= scopes)

service = build('sheets','v4',credentials=Credentials)

sheet = service.spreadsheets()

# -------------------------------

# this class groups all the funtions we can do with out API connection
# 
class Pygs:
    def __init__(self,spreadsheet_id=spreadsheet_id, sheet=sheet):
        self.spreadsheet_id = spreadsheet_id
        self.sheet = sheet

# this function return the sheet names you have in the spreadsheet
    def list_sheet_names(self):
        spreadsheet = self.sheet.get(spreadsheetId=self.spreadsheet_id).execute()
        
        sheet_names = [s['properties']['title'] for s in spreadsheet['sheets']]
        sheet_ids = [s['properties']['sheetId'] for s in spreadsheet['sheets']]
    
        return sheet_names, sheet_ids
    
# if you want to run the funtion:
# print(pg.list_sheet_names()

# --------------------------------------------

# this funtion lets us create new sheets in the spreadsheet
    def create_sheet(self, sheet_name,sheet_index=1):
        sheet_names = self.list_sheet_names()[0]
        i = random.randint(1,100)
        if sheet_name in sheet_names:
            sheet_name = f'{sheet_name} ({i})'
        body = {
            'requests':[{
                'addSheet': {
                    'properties': {
                        'title': sheet_name,
                        'index': sheet_index
                                }
                            }
                        }]
                }
        response = self.sheet.batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()
        return response
    
# if you want to run the funtion:
# print(pg.create_sheet(sheet_name='sheet1',sheet_index=(optional))

# --------------------------------------------

# this funtion lets us read inside the sheet we specify

    def read_sheet(self, sheet_name=None, sheet_range=None):
        if sheet_range is None:
            worksheet_name = sheet_name
        else:
            worksheet_range = f'{sheet_name}!{sheet_range}'
    
        response = self.sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                        range=worksheet_range).execute()
        values = response.get('values',[])
        return values
    
# if you want to run the funtion:
# print(pg.read_sheet(sheet_name='sheet1',sheet_range=(optional))

# --------------------------------------------

# this function clears the sheet we specify

    def clear_sheet(self, sheet_name=None, sheet_range=None):
        if sheet_range is None:
            worksheet_range = sheet_name
        else:
            worksheet_range = f'{sheet_name}!{sheet_range}'
    
        response = self.sheet.values().clear(spreadsheetId=self.spreadsheet_id,
                                        range=worksheet_range,
                                        body={}).execute()
    
        return response

# if you want to run the funtion:
# print(pg.clear_sheet(sheet_name='sheet1'))

# --------------------------------------------

# this funtion appends to an existing sheet

    def append_to_sheet(self, sheet_name=None, sheet_range=None, values=None):

        if sheet_range is None:
            worksheet_range = sheet_name
        
        else:
            worksheet_range = f'{sheet_name}!{sheet_range}'
        
        if all(isinstance(v, list) for v in values):
            values = values

        else:
            values = [values]

        response= self.sheet.values().append(
                            spreadsheetId = self.spreadsheet_id,
                            range =worksheet_range,
                            valueInputOption='USER_ENTERED',
                            insertDataOption='OVERWRITE',
                            body={'values': values}
                            ).execute()
        return response

# if you want to run the funtion:
# print(pg.append_to_sheet(sheet_name='sheet1',sheet_range='A5:C5',values=[1,2,3,4,5,6,7,8,9,0]))

# --------------------------------------------

# this funtion overwrites an existing sheet

    def overwrite_sheet(self, sheet_name=None, sheet_range=None, values=None):
        clear = self.clear_sheet(sheet_name=sheet_name)
        append = self.append_to_sheet(sheet_name=sheet_name, sheet_range=sheet_range , values=values)

        return clear, append

# if you want to run the funtion:
# print(pg.overwrite_sheet(sheet_name='sheet1',sheet_range=None,values=[1,2,3,4,'that coulmn',5,6,7,8,9,'this column']))

# --------------------------------------------

# this funtion move a dataframe to a sheet

    def dataframe_to_sheet(self, sheet_name=None, dataframe=None, overwrite=True):

        if overwrite:
            clear = self.clear_sheet(sheet_name=sheet_name) 
            append = self.append_to_sheet(sheet_name=sheet_name, values=dataframe.columns.tolist()) 
        else:
            clear = None
        
        append = self.append_to_sheet(sheet_name=sheet_name, values=dataframe.values.tolist())
        
        return clear, append


# a dataframe for testing dataframe_to_sheet funtion:
df = pd.read_csv('data/diamonds.csv')

# this is a great way to implement the class as a local library
pg = Pygs()

# this is how to run the funtion
#print(pg.dataframe_to_sheet(sheet_name='new sheet name', dataframe=df))



print(pg.clear_sheet(sheet_name='new sheet name'))

