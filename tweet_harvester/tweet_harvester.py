import os
import time
from dotenv import load_dotenv
from tweepy import API, OAuth2BearerHandler
from tweepy import Stream, Cursor
import pickle
import threading
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import shapefile
from shapely.geometry import Point  # Point class
from shapely.geometry import shape  # shape() is a function to convert geo objects through the interface
import couchdb
import numpy as np
import sys

area = os.environ['AREA']
query_topic = os.environ['TOPIC']
SERVER_PATH = os.environ["DB_SERVER"]
DB_NAME = os.environ["DB_NAME"]

# area = 'Melbourne - Inner South'
# query_topic = 'food'
# SERVER_PATH = 'http://admin:admin@172.26.129.26:5984/'
# DB_NAME = 'test_food1_nogeo'
# args = sys.argv
# query_topic = None
# area = None

# if len(args) < 5:
#     print("Usage: python ./twitter_harvester <Area> <Topic> <Ip> <DB_name>")
#     exit()
# else:
#     query_topic = args[2]
#     area = args[1]
#     SERVER_PATH = 'http://admin:admin@' + args[3] + ':5984'
#     DB_NAME = args[4]

#print(args)
print(query_topic, area)
print('SERVER_PATH: ', SERVER_PATH)
print('DB_name: ',DB_NAME)
dic_file = "area_coordinate.pkl"
a_file = open(dic_file, "rb")
area_coordinate_dic = pickle.load(a_file)
a_file.close()

dic_file = "area_bbxs.pkl"
a_file = open(dic_file, "rb")
area_bbxs = pickle.load(a_file)
a_file.close()

serach_coordinate = []
if area == 'Melbourne' or area == 'MEL':
    for key,coordinate_list in area_coordinate_dic.items():
        for coordinate in coordinate_list:
            serach_coordinate.append(coordinate)
else:
    if area in area_coordinate_dic:
        for coordinate in area_coordinate_dic[area]:
            serach_coordinate.append(coordinate)
    else:
        print("Area is illegal, using melbourne as default")
        for key, coordinate_list in area_coordinate_dic.items():
            for coordinate in coordinate_list:
                serach_coordinate.append(coordinate)

# #now we will Create and configure logger
# logging.basicConfig(filename="std.log",
# 					format='%(asctime)s %(message)s',
# 					filemode='w')
#
# #Let us Create an object
# logger=logging.getLogger()
#
# #Now we are going to Set the threshold of logger to DEBUG
# logger.setLevel(logging.DEBUG)


nltk.download('vader_lexicon')
SHAPE_FILE_PATH = './aurin_data/shp_files/spatialise-SA4/shp/apm_sa4_2016_timeseries-.shp'
#TWEET_DATA_PATH = r'C:\Users\thoma\Desktop\IT\CCC\A2\full_data\food.json'


tweets_list = []
threads = []

load_dotenv()
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
if not bearer_token:
    raise RuntimeError("Not found bearer token")

auth = OAuth2BearerHandler(bearer_token)
api = API(auth, wait_on_rate_limit=True)
lock = threading.Lock()
threads = []

#query_string = "food OR restaurant OR breakfast OR lunch OR dinner OR cook OR cafe"
# query_string = "covid-19 OR coronavirus OR #covid-19 OR #coronavirus"
# query_string = "market OR supermarket"
# query_string = "park"
# query_string = "melbournemoney OR #melbournemoney"
#query_string = "*"
max_id = None


def CouchDB(SERVER_PATH, DB_NAME, data_list):
    couch = couchdb.Server(SERVER_PATH)
    if DB_NAME in couch:
        db = couch[DB_NAME]
    else:
        db = couch.create(DB_NAME)

    for data in data_list:
        db.save(data)


def process_tweet(tweet_list):
    shp = shapefile.Reader(SHAPE_FILE_PATH)  # open the shapefile
    all_shapes = shp.shapes()  # get all the polygons
    all_records = shp.records()
    data_list = []
    counter = 0
    for line in tweet_list:
        counter += 1
        if counter % 1000 == 0:
            print("Finish: ", counter)
        j = line
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


def getFullText(tweet):
    if tweet.is_quote_status is True and not tweet.text.startswith("RT"):
        if 'extended_tweet' in tweet._json['retweeted_status']:
            full_text = tweet._json['retweeted_status']['extended_tweet']['full_text']
        else:
            full_text = tweet._json['retweeted_status']['text']
    elif tweet.text.startswith("RT") and tweet.retweeted_status is not None:
        if 'extended_tweet' in tweet._json['quoted_status']:
            full_text = tweet._json['quoted_status']['extended_tweet']['full_text']
        else:
            full_text = tweet._json['quoted_status']['text']
    else:
        if 'extended_tweet' in tweet._json:
            full_text = tweet._json['extended_tweet']['full_text']
        else:
            full_text = tweet._json['text']

    return {"coordinates": tweet.coordinates['coordinates'], "text": full_text}


"""
search recent 7 days tweets api v1.1
"""


def search_recent():
    num_geo_tweets = 0
    max_results = 100
    counter = 0
    resps = []
    # https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/overview
    # for i in range(2):
    print("get in search_recent")
    i = 1
    while (i):
        print("i th search", i)
        i += 1
        for coordinate in serach_coordinate:
            geocode = str(coordinate[0]) + ',' + str(coordinate[1]) + ',' + '15km'
            print("Start:",geocode)
            resp = api.search_tweets(q=query_topic, count=max_results, geocode=geocode)
            lock.acquire()

            for i, tweet in enumerate(resp):
                if tweet.coordinates is not None:
                    # resps.append(processTweet(tweet))
                    num_geo_tweets += 1
                    tweets_list.append(json.dumps(tweet._json))
            lock.release()
            while (len(resp) > 0):
                print("count", counter)
                print(len(resp))
                max_id = resp[-1].id - 1
                resp = api.search_tweets(q=query_topic, count=max_results, geocode=geocode,
                                         max_id=max_id)
                lock.acquire()
                counter += 1
                for tweet in resp:
                    if tweet.coordinates is not None:
                        tweets_list.append(json.dumps(tweet._json))
                        num_geo_tweets += 1
                    # json.dumps(tweet._json, f, indent=2)
                lock.release()
        print("end in search_recent")


    print(resps)
    print(num_geo_tweets)


"""
Stream
"""


class TweetListener(Stream):
    def on_status(self, status):
        print(status.id)
        if status.coordinates is not None:
            tweets_list.append(json.dumps(status._json))

    def on_request_error(self, status_code):
        print(status_code)

    def on_connection_error(self):
        print("connection error")
        self.disconnect()


tweetListener = TweetListener(
    os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_KEY_SECRET"),
    os.getenv("ACCESS_KEY"), os.getenv("ACCESS_KEY_SECRET")
)


def stream():
    if area == 'Melbourne' or area == 'MEL':
        tweetListener.filter(track=["{topic}".format(topic=query_topic)],
                         locations=[144.3336, -38.5030, 145.8784, -37.1751])
    elif area in area_bbxs:
        print("In ",area)
        print("Bounding box is ",area_bbxs[area])
        print(type(area_bbxs[area]))
        tweetListener.filter(track=["{topic}".format(topic=query_topic)],
                             locations=area_bbxs[area])
        print("start stream")
    else:
        print('No valid area detective, running as default melbourne')
        tweetListener.filter(track=["{topic}".format(topic=query_topic)],
                             locations=[144.3336, -38.5030, 145.8784, -37.1751])


def search_30():
    counter = 0
    try:
        if area == 'Melbourne' or area == 'MEL':
            for page in Cursor(api.search_30_day, label="dev",
                               query="place_country:Au place:Melbourne ({topic})".format(topic=query_topic)).pages(1):
                counter += 1
                lock.acquire()
                for tweet in page:
                    if tweet.coordinates is not None:
                        tweets_list.append(tweet)
                        # print(tweet.created_at, tweet.text, tweet.coordinates)
                lock.release()
        elif area in area_bbxs:
            for page in Cursor(api.search_30_day, label="dev",
                               query="bouding_box:{bbx} ({topic})".format(topic=query_topic,bbx = area_bbxs[area])).pages(1):
                counter += 1
                lock.acquire()
                for tweet in page:
                    if tweet.coordinates is not None:
                        tweets_list.append(tweet)
                        # print(tweet.created_at, tweet.text, tweet.coordinates)
                lock.release()
        else:
            print('No valid area detective, running as default melbourne')
            for page in Cursor(api.search_30_day, label="dev",
                               query="place_country:Au place:Melbourne ({topic})".format(topic=query_topic)).pages(1):
                counter += 1
                lock.acquire()
                for tweet in page:
                    if tweet.coordinates is not None:
                        tweets_list.append(tweet)
                        # print(tweet.created_at, tweet.text, tweet.coordinates)
                lock.release()

    except:
        print("requests exceed monthly maximum limit")



def check():
    global tweets_list
    check_num = 0
    dic_file = 'index_checking.pkl'

    while 1:
        lock.acquire()
        if len(tweets_list) == 0:
            print("sleep")
            lock.release()
            time.sleep(3)
        else:
            print("start check", check_num)
            if os.path.exists(dic_file):
                a_file = open(dic_file, "rb")
                index_dic = pickle.load(a_file)
                a_file.close()

            else:
                index_dic = {}
            check_num += 1
            process_tweet_list = []
            for tweet in tweets_list:
                tweet = json.loads(tweet)
                if tweet['coordinates'] is not None:
                    if tweet['id'] not in index_dic:
                        process_tweet_list.append(tweet)
                        index_dic[tweet['id']] = 0
            if len(dic_file) != 0:
                a_file = open(dic_file, "wb")
                pickle.dump(index_dic, a_file)
                a_file.close()
            tweets_list = []
            lock.release()
            if len(process_tweet_list) != 0:
                print("couchdb ready")
                CouchDB(SERVER_PATH, DB_NAME, process_tweet(process_tweet_list))

                print("end checking")


def search_full(bearerToken, label, fromDate, toDate):
    counter = 0
    bearer_token = os.getenv(bearerToken)
    if not bearer_token:
        raise RuntimeError("Not found bearer token")

    auth = OAuth2BearerHandler(bearer_token)
    api = API(auth, wait_on_rate_limit=True)

    try:
        for page in Cursor(api.search_full_archive, label=label,
                           query="place_country:Au place:Melbourne ({topic})".format(topic=query_topic),
                           fromDate=fromDate,
                           toDate=toDate).pages(1):
            counter += 1
            lock.acquire()
            for tweet in page:
                if tweet.coordinates is not None:
                    tweets_list.append(tweet)
            lock.release()

    except:
        print("requests exceed maximum limit")


# Create two threads as follows
bearer_tokens = ["TWITTER_BEARER_TOKEN", "TWITTER_BEARER_TOKEN2", "TWITTER_BEARER_TOKEN3", "TWITTER_BEARER_TOKEN4",
                 "TWITTER_BEARER_TOKEN5", "TWITTER_BEARER_TOKEN6"]
labels = ["devfull", "devleo", "JOE1", "JOE2", "dev", "dev"]
fromDates = "201704080000"
toDates = "202204080000"

if __name__ == "__main__":
    try:
        print("start")
        t0 = threading.Thread(target=search_recent)  # 7 days
        # t1 = threading.Thread(target=search_30)
        t2 = threading.Thread(target=stream)
        t3 = threading.Thread(target=check)
        # threads.append(t0)
        # threads.append(t1)
        # threads.append(t2)
        # threads.append(t3)
        t0.start()
        # t1.start()
        t2.start()
        t3.start()

        # t = threading.Thread(target=search_full, args=[bearer_tokens[i], labels[i], fromDate, toDate])
        # threads.append(t)
        #  t.start()
        [thread.join() for thread in threads]
        # tweets_list = []
        # with open("food.js", "a+") as f:
        #     for tweet in tweets:
        #         jsonStr = json.dumps(tweet._json)
        #         tweets_list.append(tweet._json)
        #         f.write(jsonStr + "\n")
        #


    except:
        print("Error: unable to start thread")

    while 1:
        pass
