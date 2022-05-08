import os
import time
from dotenv import load_dotenv
from tweepy import API, OAuth2BearerHandler
from tweepy import Stream, Cursor
import _thread
import json
import threading





def processTweet(tweet):
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

    return {"coordinates":tweet.coordinates['coordinates'], "text":full_text}

load_dotenv()
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
if not bearer_token:
    raise RuntimeError("Not found bearer token")

auth = OAuth2BearerHandler(bearer_token)
api = API(auth)

bearer_token2 = os.getenv("TWITTER_BEARER_TOKEN2")
if not bearer_token2:
    raise RuntimeError("Not found bearer token")

auth2 = OAuth2BearerHandler(bearer_token2)
api2 = API(auth2)

lock = threading.Lock()
tweets = []
threads = []
query_string = "food OR restaurant"
# query_string = "covid-19 OR coronavirus OR #covid-19 OR #coronavirus"
# query_string = "market OR supermarket"
# query_string = "park"
# query_string = "melbournemoney OR #melbournemoney"
query_string = "*"
max_id = None

"""
search recent 7 days tweets api v1.1
"""

def search_recent():

    num_geo_tweets = 0
    max_results = 100
    limit = 450
    counter = 0
    resps = []
    # https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/overview
    #for i in range(2):
    for i in range(1):

        resp = api.search_tweets(q=query_string,count=max_results, geocode="-37.81585,144.96313,150km")
        with open("test.json", 'w') as f:
            for i,tweet in enumerate(resp):
                if tweet.coordinates is not None:
                    resps.append(processTweet(tweet))
                    num_geo_tweets += 1
                jsonStr = json.dumps(tweet._json)
                f.write(jsonStr+"\n")

            while(len(resp) > 0):
                max_id = resp[-1].id - 1
                resp = api.search_tweets(q=query_string,count=max_results, geocode="-37.81585,144.96313,150km",max_id=max_id)

                counter += 1
                for tweet in resp:
                    if tweet.coordinates is not None:
                        resps.append(processTweet(tweet))
                        num_geo_tweets += 1
                    #json.dumps(tweet._json, f, indent=2)
                    jsonStr = json.dumps(tweet._json)
                    f.write(jsonStr+"\n")
                if (counter == limit):
                    print("sleep")
                    print(num_geo_tweets)
                    print(len(resps))
                    print(len(set(resps)))
                    time.sleep(15 * 60)
    # print(len(resps))
    # print(len(set(resps)))
    print(resps)
    print(num_geo_tweets)


"""
Stream
"""

class TweetListener(Stream):

    def on_status(self, status):
        #print(status.id)
        print(status.text)
        #print(status.user.id)
        #print(api.user_timeline(user_id=status.user.id))

    def on_request_error(self, status_code):
        print(status_code)

    def on_connection_error(self):
        self.disconnect()

tweetListener = TweetListener(
    os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_KEY_SECRET"),
    os.getenv("ACCESS_KEY"), os.getenv("ACCESS_KEY_SECRET")
)

def stream():
    tweetListener.filter(track=["food OR restaurant"], locations=[144.3336,-38.5030,145.8784,-37.1751])


def search_30():
    limit = 30
    counter = 0
    try:
        for page in Cursor(api2.search_30_day, label="dev",
                           query="place_country:Au place:Melbourne (food OR restaurant)").pages(1):
            counter += 1
            lock.acquire()
            for tweet in page:
                if tweet.coordinates is not None:
                    tweets.append(tweet)
                    #print(tweet.created_at, tweet.text, tweet.coordinates)
            lock.release()
            if counter == limit:
                print("requests exceed minute limit")
                time.sleep(60)
    except:
        print("requests exceed monthly maximum limit")


def search_full(bearerToken, label, fromDate, toDate):
    limit = 30
    counter = 0
    bearer_token = os.getenv(bearerToken)
    if not bearer_token:
        raise RuntimeError("Not found bearer token")

    auth = OAuth2BearerHandler(bearer_token)
    api = API(auth)

    try:
        for page in Cursor(api.search_full_archive, label=label,
                           query="place_country:Au place:Melbourne (food OR restaurant)", fromDate=fromDate,
                           toDate=toDate).pages(1):
            counter += 1
            lock.acquire()
            for tweet in page:
                if tweet.coordinates is not None:
                    tweets.append(tweet)
            lock.release()
            if counter == limit:
                print("requests exceed minute limit")
                time.sleep(60)
    except:
        print("requests exceed maximum limit")

#Create two threads as follows
bearer_tokens = ["TWITTER_BEARER_TOKEN", "TWITTER_BEARER_TOKEN2","TWITTER_BEARER_TOKEN3","TWITTER_BEARER_TOKEN4","TWITTER_BEARER_TOKEN5"]
labels = ["devfull","devleo"]
fromDates = ["202104080000", "202004080000","201904080000","201804080000","201704080000"]
toDates = ["202204080000", "202104070000","202004070000""201904070000","201804070000"]
try:
   t0 = threading.Thread(target=search_recent) # 7 days
   t1 = threading.Thread(target=search_30)
   t2 = threading.Thread(target=stream)
   threads.append(t0)
   threads.append(t1)
   threads.append(t2)
   t0.start()
   t1.start()
   t2.start()
   for i in range(5):
        t = threading.Thread(target=search_full, args=[bearer_tokens[i], labels[i], fromDates[i], toDates[i]])
        threads.append(t)
        t.start()
   [thread.join() for thread in threads]
   with open("food.js", "a+") as f:
       for tweet in tweets:
           jsonStr = json.dumps(tweet._json)
           f.write(jsonStr + "\n")
       f.close()

   #_thread.start_new_thread( search_recent, () )
   #_thread.start_new_thread(search_30, ())
   # for i in range(4):
   #     _thread.start_new_thread(bearer_tokens[i], search_full, (labels[i], fromDates[i], toDates[i]))

   #_thread.start_new_thread( stream, () )
except:
    print("Error: unable to start thread")

while 1:
    pass







