from flask import Flask, render_template, request, jsonify
from src.scrape import fetchJobs, parseData
from src.gemini import analyzeJobs
import json

app = Flask(__name__)

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
        jobTitle = request.form.get('jobTitle', '').strip()

        #fetch and then clean data
        rawData = fetchJobs(jobTitle)
        cleanData = parseData(rawData)

        #save parsed json data to file
        #with open('jobsList.json', 'w', encoding='utf-8') as f:
        #    json.dump(cleanData, f, indent=2, ensure_ascii=False)

        geminiAnalysis = analyzeJobs(cleanData, background)

        return f"AI Analysis Results:\n\n{geminiAnalysis}"

    return render_template("index.html")

# @app.route("/results")
# def scrape():
#     return render_template("results.html")