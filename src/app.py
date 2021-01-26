import flask
from flask import jsonify, request
import requests
import json

app = flask.Flask(__name__)


# Search for paper according to keywords and field of studies
@app.route('/search', methods=['POST'], endpoint="func1")
def handle_search():
    # decouple requests
    content = request.json
    keywords = content['keywords']
    fos = content['fos']
    print(keywords, fos)

    # configure request body and headers
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

    # send request to semantic
    r = requests.post('https://www.semanticscholar.org/api/1/search', data = json.dumps(payload), headers = headers)
    # parse the results
    results = r.json()['results']
    #print("results length: {}".format(len(results)))

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
            #print(counter)
            if len(specifics) == 5:
                break
        # if there are fields that doeesn't exist in current item
        except:
            pass
    return jsonify(specifics)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug = True)
