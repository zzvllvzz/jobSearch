import requests
import json

#maybe could be done using @dataclass insted of dict?

#fetch job via open API
def fetchJobs(jobTitle: str) -> dict[str, str]:
    url = "https://duunitori.fi/api/v1/jobentries"
    params = {
        "search": jobTitle,
        "search_also_descr": 1,
        "format": "json"
    }

    response = requests.get(url, params=params)

    # raise error if fail
    response.raise_for_status()

    data = response.json()

    return data

#clean the data 
def parseData(rawJobs: dict[str, str]) -> dict[str, str]:
    cleanJobs = []
    
    for job in rawJobs.get('results', []):
        #create dictionary
        parsedJobs = {
            'title': job.get('heading', ''),
            'company': job.get('company_name', ''),
            'location': job.get('municipality_name', ''),

            #check if descr over 500 chars = truncate & add ...; else do not truncate descr

            'description': job.get('descr', '')[:500] + '...' if len(job.get('descr', '')) > 500 else job.get('descr', ''),
            'date_posted': job.get('date_posted', ''),

            #slug apparantly is needed for url; slug - url title
            'slug': job.get('slug', ''),

            #create url only if slug exist; else empty 
            'url': f"https://duunitori.fi/tyopaikat/tyo/{job.get('slug', '')}" if job.get('slug') else ''
        }
        cleanJobs.append(parsedJobs)
    return cleanJobs
