from flask import Flask, render_template, request, jsonify
from src.scrape import fetchJobs, parseData
from dotenv import load_dotenv
import json
import os

# load env variables
load_dotenv()

app = Flask(__name__)
app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

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
        with open('jobsList.json', 'w', encoding='utf-8') as f:
            json.dump(cleanData, f, indent=2, ensure_ascii=False)

        return f"Found {len(cleanData)} jobs and saved to jobsList.json"

    return render_template("index.html")

@app.route("/results")
def scrape():
    return render_template("results.html")