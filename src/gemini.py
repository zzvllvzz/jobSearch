from dotenv import load_dotenv
from google import genai

import json
import os

#load gemini api key
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=GEMINI_API_KEY)

#send promt to gemini with job listenings and user input; get str that looks like json back
def analyzeJobs(jobsData: dict[str, str], userBackground: str) -> str:

    prompt = f"""
    Analyze these job listings and rank them by how well they match this user background:
    
    USER BACKGROUND:
    {userBackground}
    
    JOBS DATA:
    {json.dumps(jobsData, indent=2)}
    
    Provide a ranked list from best to worst match with:
    1. Job title and company
    2. Match score (1-10)
    3. Brief reason for the match
    4. Direct link to the job posting
    
    Return the results in a clean, easy-to-read json format.
    Use consistent keys:
    dict_keys(['rank', 'job_title', 'company', 'match_score', 'reason', 'url'])
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )
    
    return response.text

#for test purposes; if run directly = execute; else not execute
if __name__ == "__main__":
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents="Can I upload json files into you for you to analyze them with API ? Can you make jsin files and send to me?"
    )
    print(type(response.text))
    print(response.text)