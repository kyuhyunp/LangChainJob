# from langchain.agents.agent_toolkits import GmailToolkit

# toolkit = GmailToolkit()

# import os
# from constants import openapi_key
# os.environ['OPENAI_API_KEY'] = openapi_key

# from langchain import OpenAI
# from langchain.agents import initialize_agent, AgentType

# llm = OpenAI(temperature=0)

# agent = initialize_agent(   
#     tools=toolkit.get_tools(),
#     llm=llm,
#     agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
# )

# agent.run("Create a gmail draft for me that asks the receiver, Martin, how he is doing. Do not send the mail.")

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


def getEmails():
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None
  
    # The file token.pickle contains the user access token.
    # Check if it exists
    if os.path.exists('token.pickle'):
  
        # Read the token from the file and store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
  
    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
  
        # Save the access token in token.pickle file for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
  
    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)
  
    # request a list of all the messages
    # https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list
    result = service.users().messages().list(userId='me', q='after:1504483200 before:1654495199').execute()
    messages = result.get('messages')
    # messages is a list of dictionaries where each dictionary contains a message id.

    if messages is None:
        return
  
    documents = []
    # iterate through all the messages
    for msg in messages:
        # Get the message from its id
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
 
        # Get value of 'payload' from dictionary 'txt'
        payload = txt['payload']
        headers = payload['headers']

        # Look for Subject and Sender Email in the headers
        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
            if d['name'] == 'From':
                sender = d['value']

        # The Body of the message is in Encrypted format. So, we have to decode it.
        # Get the data and decode it with base 64 decoder.
        if 'parts' not in payload:
            continue
        
        parts = payload.get('parts')[0]

        if not 'body' in parts or not 'data' in parts['body']:
            continue

        data = parts['body']['data']
        data = data.replace("-","+").replace("_","/")
        decoded_data = base64.b64decode(data)


        # Now, the data obtained is in lxml. So, we will parse 
        # it with BeautifulSoup library
        soup = BeautifulSoup(decoded_data , "lxml")

        if soup is None or len(soup) == 0:
            continue

        body = soup.body()

        documents.append(Document(page_content=str(body)))



        # Printing the subject, sender's email and message
        # print("Subject: ", subject)
        # # print("From: ", sender)
        print("Message: ", body)
        print('\n')

    print(type(documents))
    print(documents)
        
  
  
getEmails()


# from llama_index import download_loader

# GmailReader = download_loader('GmailReader')
# loader = GmailReader(query="after: 1504483200 before: 1654495199 label:inbox")
# documents = loader.load_data()


# print(type(documents))
