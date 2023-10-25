from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
from bs4 import BeautifulSoup

from langchain.schema.document import Document

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
ACCESS_TOKEN = 'token.pickle'
CREDENTIALS = 'credentials.json'


# jobs-noreply@linkedin.com
# your application was sent to

GMAIL_QUERY = """
in:inbox category: primary from: jobs-noreply@linkedin.com "your application was sent to" 
after: {startDate} before: {endDate}'
"""

def get_credentials():
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None
  
    # The file token.pickle contains the user access token.
    # Check if it exists
    if os.path.exists(ACCESS_TOKEN):
  
        # Read the token from the file and store it in the variable creds
        with open(ACCESS_TOKEN, 'rb') as token:
            creds = pickle.load(token)
  
    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
  
        # Save the access token in token.pickle file for the next run
        with open(ACCESS_TOKEN, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_gmail_content(service, msg):
    # Get the message from its id
    txt = service.users().messages().get(userId='me', id=msg['id']).execute()

    # Get value of 'payload' from dictionary 'txt'
    payload = txt['payload']
    
    # The Body of the message is in Encrypted format. So, we have to decode it.
    # Get the data and decode it with base 64 decoder.
    if 'parts' not in payload:
        return ""
    
    parts = payload.get('parts')[0]

    if not 'body' in parts or not 'data' in parts['body']:
        return ""

    data = parts['body']['data']
    data = data.replace("-","+").replace("_","/")
    decoded_data = base64.b64decode(data)

    # Now, the data obtained is in lxml. So, we will parse 
    # it with BeautifulSoup library
    soup = BeautifulSoup(decoded_data , "lxml")

    if soup is None or len(soup) == 0:
        return ""

    body = str(soup.body())

    # Adding Date
    header = payload['headers']
    for item in header:
        if item['name'] == 'Date':
            msg_date = item['value']
            body += "Date of application: " + msg_date + "\n"

    return body

"""
    This function will return a list of all the messages as documents
    between start and end in the Gmail account.
    
    From https://developers.google.com/gmail/api/guides/filtering
    All dates used in the search query are interpreted as midnight on that date in the PST timezone. 
    To specify accurate dates for other timezones pass the value in seconds instead
    ex) 2014/01/01 or 1388552400
"""
def get_documents(creds, startDate, endDate):
    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)
  
    # request a list of all the messages
    # https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list
    # filters: https://support.google.com/mail/answer/7190
    query = GMAIL_QUERY.format(startDate=startDate, endDate=endDate)
    result = service.users().messages().list(userId='me', q=query).execute()
    messages = result.get('messages')
    # messages is a list of dictionaries where each dictionary contains a message id.

    if messages is None:
        return
  
    documents = []
    # iterate through all the messages
    for msg in messages:
        body = get_gmail_content(service, msg)
        if body is None or len(body) == 0:
            continue

        documents.append(Document(page_content=body))
        
    return documents
