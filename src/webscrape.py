import requests
import json
import pandas as pd

def webscrape(keywords_path, fos_path, out_path):
    print("\n")
    print(">>>>>>>>>>>>>>>>>>>>>>>> Running websraping... <<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    # Extract keywords and fields of study
    fos = json.load(open(fos_path))['fos']
    print("field of study: {}".format(fos))
    keywords = json.load(open(keywords_path))['keywords']
    print("keywords: {}".format(keywords))

    # send request to the server
    print("  => Sending requests...")
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

    print("  => Saving results...")
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
        except:
            pass
        try:
            cur['title'] = item['title']['text']
        except:
            pass
        try:
            cur['authors'] = item['structuredAuthors']
        except:
            pass
        try:
            cur['abstract'] = item['paperAbstract']['text']
        except:
            pass
        try:
            cur['date'] = item['pubDate']
        except:
            pass
        # append current paper to the list of scraped papers
        specifics.append(cur)
        counter += 1
        # if the number of scraped papers meet our needs
        if len(specifics) == 5:
            break
    # write the result to a json file
    with open(out_path, 'w') as outfile:
        json.dump(specifics, outfile)
    
    print(" => Done! Webscrape result is saved as '" + out_path + "'")
    print("\n")
