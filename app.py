from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('pageNotFound.html'), 404

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/scrape")
def scrape():
    return render_template("scrape.html")