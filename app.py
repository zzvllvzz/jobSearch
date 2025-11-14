from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import json
import os

# load env variables
load_dotenv()

app = Flask(__name__)
app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

#route for not found 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('pageNotFound.html'), 404

#landing page route
@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        #get form data
        background = request.form.get('background', '')
        job_title = request.form.get('jobTitle', '')

        print(f"Background: {background}")
        print(f"Job Title: {job_title}")

    return render_template("index.html")

@app.route("/scrape")
def scrape():
    return render_template("scrape.html")