# Generative AI Driven Job Search Log

|  Wiki | 
|:-----:|
|[<img src="https://eecs441.eecs.umich.edu/img/admin/wiki.png">][wiki_page]|

[wiki_page]: https://github.com/kyuhyunp/LangChainJob/wiki

## Main Table View
![image](https://github.com/kyuhyunp/LangChainJob/assets/70357536/eb052d77-5433-445e-8563-c20b6ef75aca)

## Export to PDF 
![image](https://github.com/kyuhyunp/LangChainJob/assets/70357536/650bdc17-92ae-4048-8fa4-1be702c40bb1)


## Features
- Query for a week of email from Gmail to load job information to table
- Manually add job information to table
- Edit or delete existing table entries
- Export to pdf

## Backend Workflow
![image](https://github.com/kyuhyunp/LangChainJob/assets/70357536/dfd2ab64-4d4b-47f6-b09d-6188028ca5ee)

After receiving a request from the frontend, the backend app calls gmail_loader to retrieve filtered emails from Gmail using the Gmail API for the specified week. Then, for each email, the app calls langchain_helper to use LangChain API to get information about the contact date, employer name, job title, and contact information. After collecting job information from every email, the app sends the data to frontend in json format.

## Server Side Event
![image](https://github.com/kyuhyunp/LangChainJob/assets/70357536/fa7b1bbe-77ac-4b12-b446-144388d292af)

Only server can send messages to client. In our use case, we do not need bidirectional communication from server to client. There is a limitation on the maximum number of connections at once, so to support a lot of users, it might require a queue of requests or an alternative approach.
