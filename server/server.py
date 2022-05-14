from flask import Flask, jsonify, abort, request, make_response, url_for, Response
import couchdb
import ast
couch = couchdb.Server("http://admin:admin@172.26.135.34:5984/")
areas = ["Melbourne - Inner", "Melbourne - Inner East", "Melbourne - Inner South","Melbourne - North East","Melbourne - North West",
             "Melbourne - Outer East","Melbourne - South East","Melbourne - West","Mornington Peninsula"]
areas2 = ["Inner", "Inner East", "Inner South","North East","North West",
             "Outer East","South East","West","Mornington Peninsula"]
from flask_cors import CORS
app = Flask(__name__, static_url_path="")
CORS(app)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/food', methods=['GET'])
def get_food():
    db = couch['food']
    results1 = db.view('area_sentiment/get_area_sentiment', reduce=True, group_level=1)
    results2 = db.view('area_sentiment/get_area_sentiment', reduce=True, group_level=2)
    results3 = db.view('area_sentiment/get_area_sentiment', reduce=True, group_level=3)
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
        x = r.key[2][1:-1].split(',')
        y = [float(x[0]), float(x[1])]
        coordinates.append(y)
    db_arin = couch['aurin']
    results = db_arin.view('area_income/get_area_income')
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

    result['num_tweets'] = tweets_results
    result['sentiments'] = sentiments
    result['coordinates'] = coordinates
    result['incomes'] = incomes


    return jsonify({'results': result})

@app.route('/park', methods=['GET'])
def get_park():
    db = couch['park']
    results1 = db.view('area_sentiment/get_area_sentiment', reduce=True, group_level=1)
    results2 = db.view('area_sentiment/get_area_sentiment', reduce=True, group_level=2)
    results3 = db.view('area_sentiment/get_area_sentiment', reduce=True, group_level=3)
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
        x = r.key[2][1:-1].split(',')
        y = [float(x[0]), float(x[1])]
        coordinates.append(y)
    db_arin = couch['aurin']
    results = db_arin.view('area_income/get_area_income')
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

    result['num_tweets'] = tweets_results
    result['sentiments'] = sentiments
    result['coordinates'] = coordinates
    result['incomes'] = incomes
    return jsonify({'results': result})



if __name__ == '__main__':
    app.run(debug=True)
