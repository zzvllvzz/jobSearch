import requests
import json

def fetchJobs():
    url = "https://duunitori.fi/api/v1/jobentries"
    params = {
        "search": "engineer",
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

if __name__ == "__main__":
    fetchJobs()
