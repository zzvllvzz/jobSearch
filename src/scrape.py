import requests
import json

#fetch job via open API
def fetchJobs(jobTitle):
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

    # print json
    print(json.dumps(data, indent=4, ensure_ascii=False))

    return data

def parseData():
    ...

if __name__ == "__main__":
    fetchJobs()
