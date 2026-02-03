# this is the libraries we need to retrive spreadsheet properties

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# os library:
# This library allows you to interact with your operating system,
# for example, access files, get the file path, etc
import os 

current_dir = os.path.dirname(os.path.realpath(__file__))
key_file = os.path.join(current_dir, 'configurations', 'red-function-478012-q6-56f3b2178e8c.json')

scopes = ['https://www.googleapis.com/auth/drive']

# this is the spreadsheet id we will work with
spreadsheet_id = '1UUtUT06eVcxj4CfMGHdZKJWxIcIyYZINXJzid8J_wO4'

# credentials
Credentials = Credentials.from_service_account_file(key_file, scopes= scopes)

service = build('sheets','v4',credentials=Credentials)

sheet_properties = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()


# this is the properties of the sheet,
# its also a tests to see of we have a connection with the json key and google speadsheets id  
print(sheet_properties)