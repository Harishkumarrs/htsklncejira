#--------------------------------------------------------------------------------#
#Project: Jira automation system
#Company: Honeywell
#Authors: Divya.V, Divyalakshmi RR, Harishkumar RS
#--------------------------------------------------------------------------------#
#Import packages
from jira import JIRA
import json
from flask import Flask,request
import re
import nltk.text
from nltk.tokenize import word_tokenize
from rake_nltk import Rake
from nltk.corpus import stopwords
import xlwt
from xlwt import Workbook
#Flask namee
app = Flask(__name__)
#Authentication options
options = {
    'server': 'https://harishkumar14.atlassian.net',
    'rest_path':'api'}
#Basic Authentication
jira = JIRA(options,basic_auth=('jiraautomation11@gmail.com', '9DavtcyaFR1bmGbwBdtT4551'))
#NlP rake
keyword_rake = Rake()
#To store stopwords in language "English"
stopWords=set(stopwords.words('english'))
#List initialization
values = []

@app.route('/')
def index():
    return "Welcome to Jira automation system"


#Create issue
#url : 127.0.0.1:5000/create?summ="<Summary data>"&desc="<Description data>"&type="<Issue Type eg:Bug or Task or Improvement or New Feature>"
@app.route('/create',methods=['GET','POST'])
def create():
    new_summary = request.args.get('summ')
    new_description = request.args.get('desc')
    new_issue_type = request.args.get('type')
    new_issue = jira.create_issue(project='SAM', summary=new_summary,
                              description=new_description, issuetype={'name': new_issue_type})
    key_of_new_issue = new_issue.key
    result = 'Key:{}'.format(new_issue.key)
    return result
#Update issue
#url : 127.0.0.1:5000/update?key="<issue_key_to_be_updated>"&summ="<Summary_to_be_updated>"&desc="<Description_to_be_updated>"
@app.route('/update',methods=['GET','POST'])
def update():
    issue_key = request.args.get('key')
    update_summary = request.args.get('summ')
    update_description = request.args.get('desc')
    update_issue = jira.issue(issue_key)
    update_issue.update(summary=update_summary, description=update_description)
    result = 'Key:{}: Summary:{}: Description:{}'.format(update_issue.key, update_issue.fields.summary,update_issue.fields.description)
    return result
#Retrive particular issue
#url = 127.0.0.1:5000/retrive?key="<Issue_key>"
@app.route('/retrive', methods=['GET','POST'])
def retrive():
    issue_key = request.args.get('key')
    issue_value = jira.issue(issue_key)
    searched_key_value = issue_value.key
    searched_summary = issue_value.fields.summary
    searched_description = issue_value.fields.description
    result = 'Key:{}: Summary:{}: Description:{}'.format(issue_value.key, issue_value.fields.summary,issue_value.fields.description)
    return result
#Delete issue
#url = 127.0.0.1:5000/delete?key="<Issue_key>"
@app.route('/delete',methods=['GET','POST'])
def delete():
    key_of_issue_to_delete = request.args.get('key')
    delete_issue = jira.issue(key_of_issue_to_delete)
    delete_issue.delete()
    return "Issue deleted successfully"
#Search
#url = 127.0.0.1:5000/search?content="<Text from user>"
@app.route('/search',methods=['GET','POST'])
def search():
    input=request.args.get('content')
    words=word_tokenize(input)
    wordsFiltered=[]
    i=1
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    sheet1.write(0,0, 'Issue ID')
    sheet1.write(0,1, 'Summary')
    sheet1.write(0,2, 'Description')
    for keywords_without_stopwords in words:
    	if keywords_without_stopwords not in stopWords:
    		wordsFiltered.append(keywords_without_stopwords)
    keywords=keyword_rake.extract_keywords_from_text(input)
    ranked_keywords=keyword_rake.get_ranked_phrases()
    for data in ranked_keywords:
    	result=re.split(r'\s',data)
    	values.extend(result)
    for issue in jira.search_issues('project = SAM', maxResults=1000):
        res = issue.fields.summary
        update_new_id = []
        for pattern in values:
            if re.search(pattern.lower(),res):
                var = issue.key
                if(var not in update_new_id):
                    update_new_id.append(issue.key)
                    sheet1.write(i,0, issue.key)
                    sheet1.write(i,1, issue.fields.summary)
                    sheet1.write(i,2,issue.fields.description)
                    i = i+1
            elif re.search(pattern.capitalize(),res):
                var = issue.key
                if(var not in update_new_id):
                    update_new_id.append(issue.key)
                    sheet1.write(i,0, issue.key)
                    sheet1.write(i,1, issue.fields.summary)
                    sheet1.write(i,2,issue.fields.description)
                    i = i+1
        wb.save('result.xls')
    return "Success"

if __name__=='__main__':
    app.run()
