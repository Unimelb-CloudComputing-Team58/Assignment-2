'''
University of Melbourne
COMP90024 Cluster and Cloud Computing
2022 Semester 1 Assignment 2

Team 58:
- (Sam)    Bin Zhang,    895427 @ Melbourne
- (Joe)    Tianhuan Lu,  894310 @ Melbourne
- (Leo)    Yicong Li,   1307323 @ Melbourne
- (Peter)  Weiran Zou,  1309198 @ Melbourne
- (Thomas) Chenhao Gu,  1147534 @ Melbourne
'''

from flask import Flask, jsonify, abort, request, make_response, url_for, Response
import couchdb
import os
#DB_SERVER=http://admin:admin@172.26.129.26:5984/
#SERVER_PATH = "http://admin:admin@172.26.132.198:5984/"
SERVER_PATH = os.environ['DB_SERVER']
couch = couchdb.Server(SERVER_PATH)
print(SERVER_PATH)
areas = ["Melbourne - Inner", "Melbourne - Inner East", "Melbourne - Inner South","Melbourne - North East","Melbourne - North West",
             "Melbourne - Outer East","Melbourne - South East","Melbourne - West","Mornington Peninsula"]
areas2 = ["Inner", "Inner East", "Inner South","North East","North West",
             "Outer East","South East","West","Mornington"]
from flask_cors import CORS
app = Flask(__name__, static_url_path="")
CORS(app)

db_food = None
db_park = None
db_aurin = None

if 'food' in couch:
    db_food = couch['food']
else:
    db_food = couch.create('food')

if 'park' in couch:
    db_park = couch['park']
else:
    db_park = couch.create('park')

if 'aurin' in couch:
    db_aurin = couch['aurin']
else:
    db_aurin = couch.create('aurin')


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/food', methods=['GET'])
def get_food():
    results1 = db_food.view('area_sentiment/get_area_sentiment', reduce=True, group_level=1)
    results2 = db_food.view('area_sentiment/get_area_sentiment', reduce=True, group_level=2)
    results3 = db_food.view('area_sentiment/get_area_sentiment', reduce=True, group_level=3)
    result = {}
    tweets_results = []
    for r in results1:
        dic = {}
        dic["area"] = r.key[0]
        dic["num_tweets"] = r.value
        tweets_results.append(dic)
    print(tweets_results)
    sentiments = []

    print('\n')
    for area in areas:
        dic = {}
        dic["area"] = area
        dic["num_positive"] = 0
        dic["num_neutral"] = 0
        dic["num_negative"] = 0
        sentiments.append(dic)
    for r in results2:
        for s in sentiments:

            if r.key[0] == s["area"]:
                if r.key[1] == "POSITIVE":
                    s["num_positive"] = r.value
                elif r.key[1] == "NEUTRAL":
                    s["num_neutral"] = r.value
                else:
                    s["num_negative"] = r.value

    coordinates = []
    for r in results3:
        if (type(r.key[2]) == str):
            x = r.key[2][1:-1].split(',')
            y = [float(x[0]), float(x[1])]
            coordinates.append(y)
        else:
            coordinates.append(r.key[2])
    results = db_aurin.view('area_income/get_area_income')
    incomes = []
    for r in results:
        dic = {}
        dic["area"] = r.key[0]
        dic["income"] = r.key[1]
        incomes.append(dic)
    # shorten area name by removing Melbourne
    for i in range(len(areas2)):
        tweets_results[i]["area"] = areas2[i]
        sentiments[i]["area"]= areas2[i]
        incomes[i]["area"]= areas2[i]

    relationships = []
    for i in range(len(areas2)):
        dic = {}
        dic["income"] = incomes[i]["income"]
        dic["positivePercentage"] = sentiments[i]["num_positive"] / (
                sentiments[i]["num_positive"] + sentiments[i]["num_negative"] + sentiments[i]["num_neutral"])
        dic["negativePercentage"] = sentiments[i]["num_negative"] / (
                sentiments[i]["num_positive"] + sentiments[i]["num_negative"] + sentiments[i]["num_neutral"])
        relationships.append(dic)
    relationships = sorted(relationships, key=lambda x: x["income"])

    result['num_tweets'] = tweets_results
    result['sentiments'] = sentiments
    result['coordinates'] = coordinates
    result['incomes'] = incomes
    result['relationships'] = relationships


    return jsonify({'results': result})

@app.route('/park', methods=['GET'])
def get_park():
    results1 = db_park.view('area_sentiment/get_area_sentiment', reduce=True, group_level=1)
    results2 = db_park.view('area_sentiment/get_area_sentiment', reduce=True, group_level=2)
    results3 = db_park.view('area_sentiment/get_area_sentiment', reduce=True, group_level=3)
    result = {}
    tweets_results = []
    for r in results1:
        dic = {}
        dic["area"] = r.key[0]
        dic["num_tweets"] = r.value
        tweets_results.append(dic)
    print(tweets_results)
    sentiments = []

    print('\n')
    for area in areas:
        dic = {}
        dic["area"] = area
        dic["num_positive"] = 0
        dic["num_neutral"] = 0
        dic["num_negative"] = 0
        sentiments.append(dic)
    for r in results2:
        for s in sentiments:

            if r.key[0] == s["area"]:
                if r.key[1] == "POSITIVE":
                    s["num_positive"] = r.value
                elif r.key[1] == "NEUTRAL":
                    s["num_neutral"] = r.value
                else:
                    s["num_negative"] = r.value

    coordinates = []
    for r in results3:
        if (type(r.key[2]) == str):
            x = r.key[2][1:-1].split(',')
            y = [float(x[0]), float(x[1])]
            coordinates.append(y)
        else:
            coordinates.append(r.key[2])
    results = db_aurin.view('area_income/get_area_income')
    incomes = []
    for r in results:
        dic = {}
        dic["area"] = r.key[0]
        dic["income"] = r.key[1]
        incomes.append(dic)

    # shorten area name by removing Melbourne
    for i in range(len(areas2)):
        tweets_results[i]["area"] = areas2[i]
        sentiments[i]["area"]= areas2[i]
        incomes[i]["area"]= areas2[i]

    relationships = []
    for i in range(len(areas2)):
        dic = {}
        dic["income"] = incomes[i]["income"]
        dic["positivePercentage"] = sentiments[i]["num_positive"] / (
                    sentiments[i]["num_positive"] + sentiments[i]["num_negative"] + sentiments[i]["num_neutral"])
        dic["negativePercentage"] = sentiments[i]["num_negative"] / (
                sentiments[i]["num_positive"] + sentiments[i]["num_negative"] + sentiments[i]["num_neutral"])
        relationships.append(dic)
    relationships = sorted(relationships, key=lambda x: x["income"])




    result['num_tweets'] = tweets_results
    result['sentiments'] = sentiments
    result['coordinates'] = coordinates
    result['incomes'] = incomes
    result['relationships'] = relationships

    return jsonify({'results': result})



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
