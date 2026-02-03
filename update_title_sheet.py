# this is the libraries we need to retrive spreadsheet properties

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# os library:
# This library allows you to interact with your operating system,
# for example, access files, get the file path, etc
import os 

import datetime as dt
current_dir = os.path.dirname(os.path.realpath(__file__))
key_file = os.path.join(current_dir, 'configurations', 'red-function-478012-q6-56f3b2178e8c.json')

scopes = ['https://www.googleapis.com/auth/drive']

# this is the spreadsheet id we will work with
spreadsheet_id = '1UUtUT06eVcxj4CfMGHdZKJWxIcIyYZINXJzid8J_wO4'

# credentials
Credentials = Credentials.from_service_account_file(key_file, scopes= scopes)

service = build('sheets','v4',credentials=Credentials)

sheet = service.spreadsheets()

# -----------
# up until here everything is the same like everythime we call google sheets API 
# -----------


# this is the past where we specify what sheet we intent to clean

# variables - we will upadate the spreadsheet title to include today's date
# this is a reporting methedology for dailty reports that we send, so we can know which date the report represent.

today = dt.datetime.today().strftime('%Y-%m-%d')
spreadsheet_title = 'python google sheets ' + today

request = sheet.batchUpdate(spreadsheetId=spreadsheet_id,
                            body={
                                'requests':[{
                                    'updateSpreadsheetProperties': {
                                        'properties': {
                                            'title': spreadsheet_title },
                                            'fields':'title'
                                    }
                                }]
                            })



response = request.execute()

print(response)
