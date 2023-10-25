from flask import Flask, Response, request
from flask_cors import cross_origin
import json

import gmail_loader
import langchain_helper
from langchain.text_splitter import RecursiveCharacterTextSplitter

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
        
        jobs = []
        memory = langchain_helper.get_memory()
        for i in range(len(documents)):
            document = documents[i]

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=0)
            splits = text_splitter.split_documents([document])

            print([splits])
            print("-------------\n\n\n\n")
            conversation_chain = langchain_helper.get_conversational_retrieval_chain(splits, memory)
            partial_response = langchain_helper.get_conversation_answer(conversation_chain)
            partial_response = partial_response.replace("System: ", "", 1).strip()
            memory.clear()

            print(partial_response)
            if partial_response is None or partial_response == "":
                continue

            job = json.loads(partial_response)
            jobs.append(job)
            print(job)
            partial_response = ""

        if len(jobs) == 0:
            return f"data: no data\n\n"

        for i in range(len(jobs)):
            try:
                jobs[i]['contactInfo'] = langchain_helper.searchURL(jobs[i]['employerName'])   
            except:
                print(f"url not found for {jobs[i]['employerName']}")       
    
        return f"data: {json.dumps(jobs)}\n\n"
    
    data = get_data(startDate, endDate)
    print(data)
    
    return Response(data, mimetype="text/event-stream")
        