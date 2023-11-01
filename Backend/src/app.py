from flask import Flask, Response, request
from flask_cors import cross_origin
import json

import gmail_loader
import langchain_helper
from langchain.text_splitter import CharacterTextSplitter

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
        
        pagination_idx = 0
        sz = len(documents)
        while sz > 0:
            jobs = []
            for i in range(min(10, sz)):
                # Each document contains at most one job information
                document = documents[i + pagination_idx * 10]

                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                texts = text_splitter.split_documents([document])
                
                job = langchain_helper.generate_job_log(texts)
                if len(job['employerName']) == 0:
                    continue

                jobs.append(job)
                print(job)

                try:
                    jobs[i]['contactInfo'] = langchain_helper.searchURL(jobs[i]['employerName'])   
                except:
                    jobs[i]['contactInfo'] = "Not Available"
    
            yield f"data: {json.dumps(jobs)}\n\n"
            sz -= min(10, sz)
            pagination_idx += 1
        
        yield f"data: no data\n\n"

    data = get_data(startDate, endDate)
    print(data)
    
    return Response(data, mimetype="text/event-stream")
        