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


from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import pandas as pd
import shapefile
from shapely.geometry import Point  # Point class
from shapely.geometry import shape  # shape() is a function to convert geo objects through the interface
import couchdb

SHAPE_FILE_PATH = r'C:\Users\thoma\Desktop\IT\CCC\A2\Assignment-2\aurin_data\shp_files\spatialise-median-house-price\shp\apm_sa4_2016_timeseries-.shp'
TWEET_DATA_PATH = r'C:\Users\thoma\Desktop\IT\CCC\A2\full_data\food.json'


def process_tweet(TWEET_FILE = TWEET_DATA_PATH):
    shp = shapefile.Reader(SHAPE_FILE_PATH)  # open the shapefile
    all_shapes = shp.shapes()  # get all the polygons
    all_records = shp.records()
    data_list = []
    counter = 0
    with open(TWEET_FILE, "r", encoding="utf-8") as fp:
        for line in fp:
            counter += 1
            if counter % 1000 == 0:
                print("Finish: ", counter)
            j = json.loads(line)
            text = j['text']
            analysis = TextBlob(text)
            score = SentimentIntensityAnalyzer().polarity_scores(text)
            neg = score['neg']
            neu = score['neu']
            pos = score['pos']
            sentiment_result = ''
            if neg > pos:
                sentiment_result = 'NEGATIVE'
            elif pos > neg:
                sentiment_result = 'POSITIVE'
            else:
                sentiment_result = 'NEUTRAL'

            point_to_check = (j['coordinates']['coordinates'][0], j['coordinates']['coordinates'][1])
            for i in range(len(all_shapes)):
                boundary = all_shapes[i]  # get a boundary polygon
                if Point(point_to_check).within(shape(boundary)):  # make a point and see if it's in the polygon
                    name = all_records[i][4]
                    data = {'id': j['id'], 'text': j['text'],
                            'coordinate': j['coordinates']['coordinates'], 'area': name,
                            'sentiment': sentiment_result, 'polarity': analysis.sentiment.polarity}
                    data_list.append(data)
    return data_list


def process_teacher_tweet(TWEET_FILE = TWEET_DATA_PATH):
    shp = shapefile.Reader(SHAPE_FILE_PATH)  # open the shapefile
    all_shapes = shp.shapes()  # get all the polygons
    all_records = shp.records()
    data_list = []
    counter = 0
    with open(TWEET_FILE, "r", encoding="utf-8") as fp:
        for line in fp:
            counter += 1
            if counter % 1000 == 0:
                print("Finish: ", counter)
            j = json.loads(line)
            text = j['doc']['text']
            analysis = TextBlob(text)
            score = SentimentIntensityAnalyzer().polarity_scores(text)
            neg = score['neg']
            neu = score['neu']
            pos = score['pos']
            sentiment_result = ''
            if neg > pos:
                sentiment_result = 'NEGATIVE'
            elif pos > neg:
                sentiment_result = 'POSITIVE'
            else:
                sentiment_result = 'NEUTRAL'

            point_to_check = (j['doc']['coordinates']['coordinates'][0], j['doc']['coordinates']['coordinates'][1])
            for i in range(len(all_shapes)):
                boundary = all_shapes[i]  # get a boundary polygon
                if Point(point_to_check).within(shape(boundary)):  # make a point and see if it's in the polygon
                    name = all_records[i][4]
                    data = {'id': j['id'], 'text': j['doc']['text'],
                            'coordinate': j['doc']['coordinates']['coordinates'], 'area': name,
                            'sentiment': sentiment_result, 'polarity': analysis.sentiment.polarity}
                    data_list.append(data)
    return data_list


SERVER_PATH = 'http://admin:admin@127.0.0.1:5984'
DB_NAME = 'twitter'
SAVE_CSV_PATH = 'food_full_data.csv'


def save_data_csv(data_list, save_file):
    df = pd.DataFrame(data_list, columns=['id', 'text', 'coordinate', 'area', 'sentiment', 'polarity'])
    df.to_csv(save_file)


def load_data_csv(load_file):
    data_list = []
    df = pd.read_csv(load_file)
    d_index = df.to_dict('index')
    for index, key in d_index.items():
        key.pop('Unnamed: 0')
        data_list.append(key)
    return data_list


def CouchDB(SERVER_PATH, DB_NAME, data_list):
    couch = couchdb.Server(SERVER_PATH)
    if DB_NAME in couch:
        db = couch[DB_NAME]
    else:
        db = couch.create(DB_NAME)

    for data in data_list:
        db.save(data)


if __name__ == "__main__":
    print('The number of line is :', sum(1 for _ in open(TWEET_DATA_PATH)))
    data_list = process_tweet()
    save_data_csv(data_list, SAVE_CSV_PATH)
    # data_list = load_data_csv('teacher_data_result.csv')

    CouchDB(SERVER_PATH, DB_NAME, data_list)
