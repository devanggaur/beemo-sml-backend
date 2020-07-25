import sys 
import requests
import tweepy as tw
import pandas as pd
import geocoder
consumer_key = 'kikqyDZVyE1hb9aWk7lLanqIO'
consumer_secret = 'R9cp0n85NyhPLffyfAQbuO0LiXcIG8yLYG3x7Jjet5g7f8rpWq'
access_token = '1276064722341617664-tZesvLfDiOA8HWHU4ztG5FOW0yHKnT'
access_token_secret = 'gqmjf0zyHDzhltUX1s2709Xeqg30S15em0A4jp13rak9S'

def authenticate_twitter():
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tw.API(auth, wait_on_rate_limit=True)

def reTweet(message, tweetId):
    api.update_status(status = message, in_reply_to_status_id = tweetId, auto_populate_reply_metadata=True)
    # api.update_status('@Shivay08126885 message',1286565361802817500)
    print({"status":"ReTweeted Successfully"})

message = sys.argv[1]
tweetId = sys.argv[2]
# message = "test data"
# tweetId= 1286568286721728518
api = authenticate_twitter()
reTweet(message, tweetId)