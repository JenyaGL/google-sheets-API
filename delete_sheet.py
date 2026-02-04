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

sheet = service.spreadsheets()

# -----------
# up until here everything is the same like everythime we call google sheets API 
# -----------

# this is the past where we spesify what to delete


# variables - this is the sheetId, you can find it in spreadsheet properties
sheet_id = '1850053363'

request = sheet.batchUpdate(spreadsheetId=spreadsheet_id,
                            body={"requests":
                            [{"deleteSheet":
                            {"sheetId":sheet_id
                            }
                            }]
                            })



response = request.execute()

# this is the response, after running it we will see a new sheet named (new sheet name) in our google spreadsheet 
# its also a tests to see of we have a connection with the json key and google speadsheets id  
print(response)
