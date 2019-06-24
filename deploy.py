from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import (StringField, StringField,  RadioField, SelectField, SubmitField)
from wtforms.validators import DataRequired
import requests
import json
import re
import nltk.text
from nltk.tokenize import word_tokenize
from rake_nltk import Rake
from nltk.corpus import stopwords
from flask import Flask,request
app = Flask(__name__)

url5 = "https://klncehtsjira.atlassian.net/rest/api/3/issue/SAM-3/comment"
url6 = "https://klncehtsjira.atlassian.net/rest/api/3/issue/SAM-3/assignee"

headers = {
           "Accept": "application/json",
           "Content-Type": "application/json",}
#---URL---#
url = "https://klncehtsjira.atlassian.net/rest/api/3/issue/"
jql = "https://klncehtsjira.atlassian.net/rest/api/3/search?jql="
#--- dictionaries---#
webretrieveval={}
websearchresult = {"issue":[]}
#--Function to add results in dictionaty--#
def webresult(fwebsearchdetails):
    websearchresult["issue"].append(fwebsearchdetails)
    return


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

class InfoForm(FlaskForm):

    summary = StringField('Summary',validators=[DataRequired()])
    description = StringField('Description',validators=[DataRequired()])
    issuetype = RadioField('Issuetype', choices=[('one','Task'),('two','Bug'),('three','Story')])
    priority = SelectField('Select',
                          choices=[('Highest', 'Highest'), ('High', 'High'),('Medium', 'Medium'),('Low', 'Low'),
                                   ('Lowest', 'Lowest')])
    submit = SubmitField('Submit')

class DelForm(FlaskForm):

    key = StringField('Id:',validators=[DataRequired()])
    submit = SubmitField('Submit')

class ReForm(FlaskForm):

    kid = StringField('Id:',validators=[DataRequired()])
    submit = SubmitField('Submit')

class UpForm(FlaskForm):

    key2 = StringField('Id:',validators=[DataRequired()])
    summa = StringField('Summary',validators=[DataRequired()])
    submit = SubmitField('Submit')

class ComForm(FlaskForm):
    key1 = StringField('Id:',validators=[DataRequired()])
    para = StringField('Comment',validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def start():
    return("Welcome to jira Automation")



@app.route('/create', methods=['GET', 'POST'])
def index():

    form = InfoForm()

    if form.validate_on_submit():
        summ = form.summary.data
        desc = form.description.data
        iss = form.issuetype.data
        if(iss=="one"):
            itype = "Task"
        elif(iss=="two"):
            itype = "Bug"
        else:
            itype = "Story"
        prior= form.priority.data
        headers = {
       "Accept": "application/json",
       "Authorization":"Basic"+" "+"amlyYWF1dG9tYXRpb24xMUBnbWFpbC5jb206amlyQHV0b21hdGlvbg==",
       "Content-Type": "application/json"
         }

        payload = json.dumps( {
          "fields": {
            "summary": summ,
            "issuetype": {
              "name": itype,
            },
            "project": {
              "key": "SAM"
            },
            "description": {
              "type": "doc",
              "version": 1,
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    {
                      "text": desc,
                      "type": "text"
                    }
                  ]
                }
              ]
            },
            "priority": {
                 "name": prior
             },
          }
        } )
        url1 = "https://klncehtsjira.atlassian.net/rest/api/3/issue"
        response = requests.request(
           "POST",
           url1,
           data=payload,
           headers=headers
        )
        return(json.dumps(json.loads(response.text),sort_keys=True, indent=4, separators=(",", ": ")))
    return render_template('test.html', form=form)
#----------------------------------------------------------
@app.route('/update', methods=['GET', 'POST'])

def update():

    form = UpForm()

    if form.validate_on_submit():
        headers = {
           "Accept": "application/json",
           "Authorization":"Basic"+" "+"amlyYWF1dG9tYXRpb24xMUBnbWFpbC5jb206amlyQHV0b21hdGlvbg==",
           "Content-Type": "application/json",

        }
        key2 = form.key2.data
        summa = form.summa.data
        session['key2'] = form.key2.data
        session['summa'] = form.summa.data
        payload = json.dumps( {
          "update": {
            "summary": [
              {
                "set": summa
              }
            ]
          }
        } )
        url4 = "https://klncehtsjira.atlassian.net/rest/api/3/issue/"
        response = requests.request(
           "PUT",
           url4 + key2 ,
           data=payload,
           headers=headers
        )
        return redirect(url_for("updated"))
    return render_template('test6.html', form=form)

@app.route('/updated')
def updated():

    return render_template('updated.html')
#----------------------------------------------------------
#retrieve issue
@app.route('/retrieve', methods=['GET', 'POST'])
def retrieve():

    form = ReForm()

    if form.validate_on_submit():
        headers = {
           "Accept": "application/json",
           "Authorization":"Basic"+" "+"amlyYWF1dG9tYXRpb24xMUBnbWFpbC5jb206amlyQHV0b21hdGlvbg==",
           "Bearer": "<access_token>"
        }
        kid = form.kid.data
        session['kid'] = form.kid.data
        url2 = "https://klncehtsjira.atlassian.net/rest/api/3/issue/"
        response = requests.request(
           "GET",
           url2 + kid,
           headers=headers
        )
        test = json.loads(response.text)
        test1 = test["fields"]["description"]["content"][0]["content"][0]["text"]
        print(test1)
        print(test["fields"]["issuetype"]["name"])
        test2 = [li["body"]["content"][0]["content"][0]["text"] for li in test ["fields"]["comment"]["comments"]]
        print(test2)
        result=test["fields"]["issuetype"]["name"]
        #return("success")
    return render_template('test2.html', form=form)


#----------------------------------------------------------
#delete issue
@app.route('/delete', methods=['GET', 'POST'])
def delete():

    form = DelForm()

    if form.validate_on_submit():
        headers = {
           "Accept": "application/json",
           "Authorization":"Basic"+" "+"amlyYWF1dG9tYXRpb24xMUBnbWFpbC5jb206amlyQHV0b21hdGlvbg==",
           "Content-Type": "application/json"
        }
        key = form.key.data
        session['key'] = form.key.data
        url3 = "https://klncehtsjira.atlassian.net/rest/api/3/issue/"
        response = requests.request(
           "DELETE",
           url3 + key,
           headers=headers
        )
        print(response.text)
        return redirect(url_for("deleted"))

    return render_template('test1.html', form=form)

@app.route('/deleted')
def deleted():

    return render_template('deleted.html')
#------------------------------------------------------------
@app.route('/comment', methods=['GET','POST'])
def comment():
    form = ComForm()

    if form.validate_on_submit():
        headers = {
           "Accept": "application/json",
           "Authorization":"Basic"+" "+"amlyYWF1dG9tYXRpb24xMUBnbWFpbC5jb206amlyQHV0b21hdGlvbg==",
           "Content-Type": "application/json"
        }
        key1 = form.key1.data
        para = form.para.data
        session['key1'] = form.key1.data
        session['para'] = form.para.data
        url5 = "https://klncehtsjira.atlassian.net/rest/api/3/issue/"
        payload = json.dumps( {
          "body": {
            "type": "doc",
            "version": 1,
            "content": [
              {
                "type": "paragraph",
                "content": [
                  {
                    "text":para ,
                    "type": "text"
                  }
                ]
              }
            ]
          }
        } )
        response = requests.request(
           "POST",
           url5 + key1 + "/comment",
           data=payload,
           headers=headers
        )
        cmmt = json.loads(response.text)
        cmmt1 = cmmt["body"]["content"][0]["content"][0]["text"]
        cmmt2 = cmmt["id"]
        print(cmmt2)
        print(cmmt1)
        return redirect(url_for("comments"))
    return render_template('test4.html', form=form)

@app.route('/comments')
def comments():

    return render_template('comment.html')

#-----------------------webservice----------------------#
#--Create--#
@app.route('/webcreate',methods=['POST'])
def webcreate():
    #--Receiving data--#
    data = request.get_json()
    #--Extraction of data--#
    summary = data['summary']
    description = data['description']
    issuetype = data['issuetype']
    if 'priority' in data:
        priority = data['priority']
    else:
        priority = "Medium"
    if 'reporter' in data:
        if data['reporter'] == "klnce.emailautomation@gmail.com":
            headers["Authorization"] ="Basic"+" "+"a2xuY2UuZW1haWxhdXRvbWF0aW9uQGdtYWlsLmNvbTplbWFpbGF1dG9tYXRpb24="
    else:
        headers["Authorization"] ="Basic"+" "+"amlyYWF1dG9tYXRpb24xMUBnbWFpbC5jb206amlyQHV0b21hdGlvbg=="
    #--Payload--#
    payload = json.dumps( {
  "fields": {
    "summary": summary,
    "issuetype": {
      "name": issuetype
    },
    "project": {
      "key": "SAM"
    },
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "text": description,
              "type": "text"
            }
          ]
        }
      ]
    },
   "priority": {
     "name": priority
    },
    }
    } )
    #---Request--#
    response = requests.request("POST",url,data=payload,headers=headers)
    return(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

#--Delete--#
@app.route('/webdelete',methods=['POST'])
def webdelete():
    data = request.get_json()
    key = data['key']
    if 'reporter' in data:
        if data['reporter'] == "klnce.emailautomation@gmail.com":
            headers["Authorization"] ="Basic"+" "+"a2xuY2UuZW1haWxhdXRvbWF0aW9uQGdtYWlsLmNvbTplbWFpbGF1dG9tYXRpb24="
    else:
        headers["Authorization"] ="Basic"+" "+"amlyYWF1dG9tYXRpb24xMUBnbWFpbC5jb206amlyQHV0b21hdGlvbg=="
    response = requests.request("DELETE",url+key,headers=headers)
    print(response.status_code)
    if response.status_code is 204:
        return("Issue deleted")
    return(response.text)

#--Retrieve--#
@app.route('/webretrieve',methods=['POST'])
def webretrieve():
    data = request.get_json()
    key = data['key']
    if 'reporter' in data:
        if data['reporter'] == "klnce.emailautomation@gmail.com":
            headers["Authorization"] ="Basic"+" "+"a2xuY2UuZW1haWxhdXRvbWF0aW9uQGdtYWlsLmNvbTplbWFpbGF1dG9tYXRpb24="
    else:
        headers["Authorization"] ="Basic"+" "+"amlyYWF1dG9tYXRpb24xMUBnbWFpbC5jb206amlyQHV0b21hdGlvbg=="
    response = requests.request("GET",url+key,headers=headers)
    if response.status_code is 200:
        temp = json.loads(response.text)
        webretrieveval["key"] = temp["key"]
        webretrieveval["summary"] = temp["fields"]["summary"]
        webretrieveval["description"] = temp["fields"]["description"]["content"][0]["content"][0]["text"]
        webretrieveval["issuetype"] = temp["fields"]["issuetype"]["name"]
        webretrieveval["status"] = temp["fields"]["status"]["statusCategory"]["name"]
        comment = [li["body"]["content"][0]["content"][0]["text"] for li in temp["fields"]["comment"]["comments"]]
        webretrieveval["comments"] = comment
        result=json.dumps(webretrieveval)
        return(result)
    return(response.text)
#--Update--#
@app.route('/webupdate',methods=['POST'])
def webupdate():
    psummary = ""
    pissuetype = ""
    pdescription = ""
    ppriority=""
    data = request.get_json()
    key = data['key']
    if 'reporter' in data:
        if data['reporter'] == "klnce.emailautomation@gmail.com":
            headers["Authorization"] ="Basic"+" "+"a2xuY2UuZW1haWxhdXRvbWF0aW9uQGdtYWlsLmNvbTplbWFpbGF1dG9tYXRpb24="
    else:
        headers["Authorization"] ="Basic"+" "+"amlyYWF1dG9tYXRpb24xMUBnbWFpbC5jb206amlyQHV0b21hdGlvbg=="
    #---Get issue details---#
    tempresponse = requests.request("GET",url+key,headers=headers)
    if tempresponse.status_code is 200:
        temp = json.loads(tempresponse.text)
        tempsummary = temp["fields"]["summary"]
        tempdescription = temp["fields"]["description"]["content"][0]["content"][0]["text"]
        tempissuetype = temp["fields"]["issuetype"]["name"]
        temppriority = temp["fields"]["priority"]["name"]

    else:
        return(tempresponse.text)
    #---check for summary---#
    if 'summary' in data:
            psummary = data['summary']
    else:
        psummary = tempsummary
    #--check for description--#
    if 'description' in data:
        pdescription = data['description']
    else:
        pdescription = tempdescription
    #--check for issuetype--#
    if 'issuetype' in data:
        pissuetype = data['issuetype']
    else:
        pissuetype = tempissuetype
    #--check for priority--#
    if 'priority' in data:
        ppriority = data['priority']
    else:
        ppriority = temppriority
    if 'reporter' in data:
        if data['reporter'] == "klnce.emailautomation@gmail.com":
            headers["Authorization"] ="Basic"+" "+"a2xuY2UuZW1haWxhdXRvbWF0aW9uQGdtYWlsLmNvbTplbWFpbGF1dG9tYXRpb24="
    else:
        headers["Authorization"] ="Basic"+" "+"amlyYWF1dG9tYXRpb24xMUBnbWFpbC5jb206amlyQHV0b21hdGlvbg=="

    payload = json.dumps( {
          "update": {
            "summary": [
              {
                "set": psummary
              }
            ]
          },
          "fields": {
        "description":{
         "type": "doc",
          "version": 1,
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": pdescription
                }
              ]
            }
          ]
         },
         "issuetype":{
         "name":pissuetype
         },
         "priority":{
         "name":ppriority
         }
         }
        } )
     #--- API call--#
    response = requests.request("PUT",url+key,data=payload,headers=headers)
    if response.status_code is 204:
        return("Updated successfully")
    return(response.text)
#-- update status --#
@app.route('/webstatus',methods=['POST'])
def webstatus():
    pstatus = ""
    data = request.get_json()
    key = data['key']
    status = data['status']
    if status == "Backlog":
        pstatus = "11"
    if status == "Selected for Development":
        pstatus = "21"
    if status == "In Progress":
        pstatus ="31"
    if status == "Done":
        pstatus = "41"
    if 'reporter' in data:
        if data['reporter'] == "klnce.emailautomation@gmail.com":
            headers["Authorization"] ="Basic"+" "+"a2xuY2UuZW1haWxhdXRvbWF0aW9uQGdtYWlsLmNvbTplbWFpbGF1dG9tYXRpb24="
    else:
        headers["Authorization"] ="Basic"+" "+"amlyYWF1dG9tYXRpb24xMUBnbWFpbC5jb206amlyQHV0b21hdGlvbg=="

    payload = json.dumps({"transition": {"id":pstatus}})
    response = requests.request("POST",url+key+"/transitions",data=payload,headers=headers)

    if response.status_code is 204:
        return("Status updated")
    return(response.text)

#-- add comment--#
@app.route('/webaddcomment',methods=['POST'])
def webaddcomment():
    webcommentid={}
    data = request.get_json()
    key = data['key']
    if 'reporter' in data:
        if data['reporter'] == "klnce.emailautomation@gmail.com":
            headers["Authorization"] ="Basic"+" "+"a2xuY2UuZW1haWxhdXRvbWF0aW9uQGdtYWlsLmNvbTplbWFpbGF1dG9tYXRpb24="
    else:
        headers["Authorization"] ="Basic"+" "+"amlyYWF1dG9tYXRpb24xMUBnbWFpbC5jb206amlyQHV0b21hdGlvbg=="
    comment = data['comment']
    payload = json.dumps( {
          "body": {
            "type": "doc",
            "version": 1,
            "content": [
              {
                "type": "paragraph",
                "content": [
                  {
                    "text":comment ,
                    "type": "text"
                  }
                ]
              }
            ]
        }
    } )
    response = requests.request("POST",url+key+"/comment",data=payload,headers=headers)
    print(response.status_code)
    if response.status_code is 201:
        temp = json.loads(response.text)
        webcommentid["comment id"] = temp["id"]
        return(json.dumps(webcommentid))
    return(response.text)
#--Search by paragraph--#
@app.route('/websearch', methods=['POST'])
def websearch():
    #---Get data from user--#
    data = request.get_json()

    if 'reporter' in data:
        if data['reporter'] == "klnce.emailautomation@gmail.com":
            headers["Authorization"] ="Basic"+" "+"a2xuY2UuZW1haWxhdXRvbWF0aW9uQGdtYWlsLmNvbTplbWFpbGF1dG9tYXRpb24="
    else:
        headers["Authorization"] ="Basic"+" "+"amlyYWF1dG9tYXRpb24xMUBnbWFpbC5jb206amlyQHV0b21hdGlvbg=="

    webreserved = ["abort", "access", "add", "after", "alias", "all", "alter", "and", "any", "as", "asc", "audit", "avg", "before", "begin", "between", "boolean", "break", "by", "byte", "catch", "cf", "char", "character", "check", "checkpoint", "collate", "collation", "column", "commit", "connect", "continue", "count", "create", "current", "date", "decimal", "declare", "decrement", "default", "defaults", "define", "delete", "delimiter", "desc", "difference", "distinct", "divide", "do", "double", "drop", "else", "empty", "encoding", "end", "equals", "escape", "exclusive", "exec", "execute", "exists", "explain", "false", "fetch", "file", "field", "first", "float", "for", "from", "function", "go", "goto", "grant", "greater", "group", "having", "identified", "if", "immediate", "in", "increment", "index", "initial", "inner", "inout", "input", "insert", "int", "integer", "intersect", "intersection", "into", "is", "isempty", "isnull", "join", "last", "left", "less", "like", "limit", "lock", "long", "max", "min", "minus", "mode", "modify", "modulo", "more", "multiply", "next", "noaudit", "not", "notin", "nowait", "null", "number", "object", "of", "on", "option", "or", "order", "outer", "output", "power", "previous", "prior", "privileges", "public", "raise", "raw", "remainder", "rename", "resource", "return", "returns", "revoke", "right", "row", "rowid", "rownum", "rows", "select", "session", "set", "share", "size", "sqrt", "start", "strict", "string", "subtract", "sum", "synonym", "table", "then", "to", "trans", "transaction", "trigger", "true", "uid", "union", "unique", "update", "user", "validate", "values", "view", "when", "whenever", "where", "while", "with"]
    keyword_rake = Rake()
    stopWords=set(stopwords.words('english'))
    values = []
    input = ""
    if 'search' in data:
        input = data['search']
    #--NLP process--#
    words = word_tokenize(input)
    wordsFiltered = []
    for keywords_without_stopwords in words:
        if keywords_without_stopwords not in stopWords:
            wordsFiltered.append(keywords_without_stopwords)
    keywords = keyword_rake.extract_keywords_from_text(input)
    ranked_keywords = keyword_rake.get_ranked_phrases()
    for data in ranked_keywords:
        result = re.split(r'\s', data)
        values.extend(result)
    for word in webreserved:
        if word in values:
            values.remove(word)
    #--JQL Search--#
    websearchkey=[]
    for iteration in values :
        response = requests.request("GET",jql + "(summary~"+iteration+")"+"OR"+"(description~"+ iteration+")"+"OR"+"(comment~"+ iteration+")",headers=headers)
        keyid = json.loads(response.text)
        kval = [li["key"] for li in keyid["issues"]]
        for temp in kval:
            if temp not in websearchkey:
                websearchkey.append(temp)

    if len(websearchkey) is 0:
        return("{"+"Error:No issues match for search"+"}")

    #--Data retrieval--#
    for val in websearchkey:
        websearchdetails = {}
        result = requests.request("GET",url+val,headers=headers)
        nresponse = json.loads(result.text)
        websearchdetails["key"] = val
        summ = nresponse["fields"]["summary"]
        websearchdetails["summary"]=summ
        desc = nresponse["fields"]["description"]["content"][0]["content"][0]["text"]
        websearchdetails["description"]=desc
        itype = nresponse["fields"]["issuetype"]["name"]
        websearchdetails["issue type"]=itype
        status = nresponse["fields"]["status"]["statusCategory"]["name"]
        websearchdetails["status"]=status
        comm = [li["body"]["content"][0]["content"][0]["text"] for li in nresponse["fields"]["comment"]["comments"]]
        websearchdetails["comment"]=comm
        webresult(websearchdetails)

    if result.status_code is 200:
        finalresult = json.dumps(websearchresult)
        websearchresult["issue"].clear()
        return(finalresult)
    return(result.text)



if __name__ == '__main__':
    app.run(debug=True)
