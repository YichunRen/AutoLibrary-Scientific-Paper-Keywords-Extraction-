import os
import requests
import json
import pandas as pd

def webscrape():
    print("\n")
    print(">>>>>>>>>>>>>>>>>>>>>>>> Running Web-sraping... <<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    # Extract keywords and fields of study
    fos = ['art']
    data = pd.read_csv("weighted_AutoPhrase.csv", index_col = "Unnamed: 0")
    keywords = data['phrase'].iloc[0]
    print("keywords: {}".format(keywords))

    # send request to the server
    print(">>>>>> Sending requests <<<<<<")
    payload = {
        "queryString":keywords,
        "page":1,
        "pageSize":10,
        "sort":"relevance",
        "authors":[],
        "coAuthors":[],
        "venues":[],
        "yearFilter":None,
        "requireViewablePdf":False,
        "publicationTypes":[],
        "externalContentTypes":[],
        "fieldsOfStudy":fos,
        "useFallbackRankerService":False,
        "useFallbackSearchCluster":False,
        "hydrateWithDdb":True,
        "includeTldrs":True,
        "performTitleMatch":True,
        "includeBadges":True
    }
    headers = {
        "Content-Type": "application/json",
        'Accept': 'application/json',
    }
    r = requests.post("https://www.semanticscholar.org/api/1/search", json.dumps(payload), headers = headers)

    # parse the results
    results = r.json()['results']

    # parse the specification of the results
    specifics = []
    counter = 0
    for item in results:
        cur = {}
        # parse useful tags
        try:
            cur['link'] = item['primaryPaperLink']['url']
            cur['title'] = item['title']['text']
            cur['authors'] = item['structuredAuthors']
            cur['abstract'] = item['paperAbstract']['text']
            specifics.append(cur)
            counter += 1
            if len(specifics) == 1:
                break
        # if there are fields that doeesn't exist in current item
        except:
            pass
    print(json.dumps(specifics))