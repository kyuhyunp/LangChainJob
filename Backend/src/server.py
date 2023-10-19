from flask import Flask, Response, request
from flask_cors import cross_origin
import json

import gmail_loader
import langchain_helper

CONVERSATION_QS = ["What company did I apply to?", "On what date did I apply?", "What position did I apply for?"]
AGENT_QS = ["What is the URL address of the company?"]


app = Flask(__name__)


@app.route("/queryWeek")
@cross_origin(origin=['http://localhost:3000'])
def stream():
    if request.args.get('start') is None or request.args.get('end') is None:
        print("Bad Request")
        return Response(status=400)
    
    startDate = request.args.get('start')
    endDate = request.args.get('end')
    
    def get_data(start, end):
        creds = gmail_loader.get_credentials()
        
        documents = gmail_loader.get_documents(creds=creds, startDate=start, endDate=end)
        if documents is None:
            return f"data: no data\n\n"
        
        memory = langchain_helper.get_memory()
        conversation_chain = langchain_helper.get_conversational_retrieval_chain(documents, memory)
        
        ret = {}
        for query in CONVERSATION_QS:
            answer = langchain_helper.get_conversation_answer(conversation_chain, query)
            ret[query] = answer

        agent_chain = langchain_helper.get_agent_chain(memory)
        for query in AGENT_QS:
            answer = langchain_helper.get_agent_answer(agent_chain, query)
            ret[query] = answer

        return f"data: {json.dumps(ret)}\n\n"
    
    #get_data(start=startDate, end=endDate)

    ret = [
        {
            "date": "10-01-2023",
            "employerName": "Google",
            "jobTitle": "Software Engineer",
            "contactInfo": "https://www.google.com"
        },
        {
            "date": "10-02-2023",
            "employerName": "Microsoft",
            "jobTitle": "Software Engineer",
            "contactInfo": "https://www.microsoft.com"
        }
    ]

    data = f"data: {json.dumps(ret)}\n\n"
    
    return Response(data, mimetype="text/event-stream")
        