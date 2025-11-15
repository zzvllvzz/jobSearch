from flask import Flask, render_template, request, jsonify
from flask import redirect, session, url_for
from src.scrape import fetchJobs, parseData
from src.gemini import analyzeJobs
from dotenv import load_dotenv

import json
import os
import re

app = Flask(__name__)

#load session key
load_dotenv()
app.secret_key = os.getenv('SESSION_SECRET_KEY')

#route for not found 404
@app.errorhandler(404)
def notFound(error):
    return render_template('pageNotFound.html'), 404

#landing page route
@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        #get html form data from user input
        background = request.form.get('background', '')
        jobTitle = request.form.get('jobTitle', '')

        #fetch and then clean data
        rawData = fetchJobs(jobTitle)
        cleanData = parseData(rawData)

        geminiAnalysis = analyzeJobs(cleanData, background)

        # store analysis in flask session
        session['analysis'] = geminiAnalysis
        session['jobTitle'] = jobTitle

        return redirect(url_for('results'))

    return render_template("index.html")

@app.route("/results")
def results():
    # analysis from flask session
    analysis = session.get('analysis', 'No analysis results found.')
    jobTitle = session.get('jobTitle', 'Unknown job title')
    
    #try/except 
    try:
        # parse json from ai response
        jsonMatch = re.search(r'\[.*\]', analysis, re.DOTALL)
        if jsonMatch:
            jobsData = json.loads(jsonMatch.group())
            print(jobsData[0].keys())
        else:
            jobsData = None
    except:
        jobsData = None
    
    #pass vars to results.html
    return render_template("results.html", 
                         analysis=analysis, 
                         jobTitle=jobTitle,
                         jobsData=jobsData)