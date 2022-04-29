import os
import time
from dotenv import load_dotenv
from tweepy import API, OAuth2BearerHandler
from tweepy import Stream
import _thread

load_dotenv()
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
if not bearer_token:
    raise RuntimeError("Not found bearer token")

auth = OAuth2BearerHandler(bearer_token)
api = API(auth)

"""
search tweets api v1.1
"""
def search_recent():
    max_results = 10
    limit = 1
    counter = 0
    resps = []
    # https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/overview
    #for i in range(2):
    resp = api.search_tweets(q="*",count=max_results, geocode="-37.81585,144.96313,150km")
    while(1):
        max_id = resp[-1].id - 1
        resp = api.search_tweets(q="*",count=max_results, geocode="-37.81585,144.96313,150km",max_id=max_id)
        resps += resp
        counter += 1
        if (counter == limit):
            for tweet in resp:
                print(tweet.id)
            time.sleep(15*60)




"""
Stream
"""

class TweetListener(Stream):

    def on_status(self, status):
        print(status.id)
        print(status.text)

    def on_request_error(self, status_code):
        print(status_code)

    def on_connection_error(self):
        self.disconnect()

tweetListener = TweetListener(
    os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_KEY_SECRET"),
    os.getenv("ACCESS_KEY"), os.getenv("ACCESS_KEY_SECRET")
)
# #144.580536,-38.48089,145.396615,-37.571382
def stream():
    tweetListener.filter(locations=[144.58,-38.48,145.39,-37.57])

#tweetListener.sample()

# Create two threads as follows
try:
   _thread.start_new_thread( search_recent, () )
   _thread.start_new_thread( stream, () )
except:
    print("Error: unable to start thread")

while 1:
   pass
"""
search_30_day
"""
# print(len(resps))
# print(len(set(resps)))
#print(resps)
# starttime = time.time()
# resp2 = []
# while(1):
#     resp = api.search_30_day(label="dev", query="Melbourne", maxResults=max_results)
#     # for tweet in resp:
#     #     #if tweet.geo is not None:
#     #     print(tweet.created_at, tweet.text, tweet.geo)
#     resp2 += resp
#     counter+=1
#     print(counter)
#     if counter == 30:
#         print(len(resp))
#         print(len(set(resp2)))
#         print(time.time()-starttime)
#         time.sleep(60-(time.time()-starttime))


