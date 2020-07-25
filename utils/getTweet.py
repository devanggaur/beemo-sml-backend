import sys 
import requests
import tweepy as tw
import pandas as pd
import geocoder
import paralleldots

paralleldots_api_key = '5YDm2Xt4aF1xj8PScqADQnlLbiu9EgPjZROD9YZQr6o'
paralleldots.set_api_key(paralleldots_api_key)

consumer_key = 'kikqyDZVyE1hb9aWk7lLanqIO'
consumer_secret = 'R9cp0n85NyhPLffyfAQbuO0LiXcIG8yLYG3x7Jjet5g7f8rpWq'
access_token = '1276064722341617664-tZesvLfDiOA8HWHU4ztG5FOW0yHKnT'
access_token_secret = 'gqmjf0zyHDzhltUX1s2709Xeqg30S15em0A4jp13rak9S'

state_code = {
    "Jharkhand" : "IN-JH",
    "West Bengal": "IN-WB",
    "Madhya Pradesh" : "IN-MP",
    "Uttar Pradesh" : "IN-UP",
    "Karnataka": "IN_KA",
    "Andhra Pradesh": "IN-AP",
    "Arunachal Pradesh" :	"IN-AR",
    "Assam"	:"IN-AS",
    "Bihar"	: "IN-BR",
    "Chandigarh"	:	"IN-CH",
    "Chhattisgarh":	"IN-CT",
    "Dadra and Nagar Haveli":	"IN-DN",
    "Daman and Diu" : "IN-DD",
    "Delhi"	:	"IN-DL",
    "Goa" : "IN-GA",
    "Gujarat" :	"IN-GJ",
    "Haryana"	: "IN-HR",
    "Himachal Pradesh" : "IN-HP",
    "Jammu and Kashmir": "IN-JK",
    "Kerala" :	"IN-KL",
    "Lakshadweep" :	"IN-LD",
    "Madhya Pradesh" :	"IN-MP",
    "Maharashtra"	: "IN-MH",
    "Manipur" :	"IN-MN",
    "Meghalaya"	: "IN-ML",
    "Mizoram" :	"IN-MZ",
    "Nagaland" : "IN-NL",
    "Odisha" :	"IN-OR",
    "Puducherry" : "IN-PY",
    "Punjab" : "IN-PB",
    "Rajasthan" : "IN-RJ",
    "Sikkim" : "IN-SK",
    "Tamil Nadu"	: "IN-TN",
    "Telangana"	: "IN-TG",
    "Tripura"	: "IN-TR",
    "Uttarakhand" : "IN-UT",
    "Uttaranchal" : "IN-UT"
}

def sentiments(message):
    sentiment = paralleldots.sentiment( message )['sentiment']
    print(sentiment)
    if(sentiment['positive'] < sentiment['negative']):
        if(sentiment['negative'] < sentiment['neutral']):
            return 0
        else:
            return -1
    elif(sentiment['negative'] < sentiment['positive']):
        if(sentiment['positive'] < sentiment['neutral']):
            return 0
        else:
            return 1

def authenticate_twitter():
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tw.API(auth, wait_on_rate_limit=True)

def getTweets(search_words, date_since):
    tweets = tw.Cursor(api.search,
                q=search_words,
                include_entities=True,
                lang="en",
                since=date_since).items(50)
    return tweets

search_words = "India Employment"
date_since = "2020-07-01"


# users = tw.Cursor(api.me)

api = authenticate_twitter()
tweets = getTweets(search_words, date_since)

tweetResponse = []
for tweet in tweets:
    
    tweet_data = {}
    if(len(tweet.entities['urls'])):
        tweet_data['tweet_url'] = tweet.entities['urls'][0]['url']
    status = api.get_status(tweet.id, tweet_mode="extended")
    try:
        tweet_data['message'] = status.retweeted_status.full_text
    except AttributeError:  # Not a Retweet
        tweet_data['message'] = status.full_text
    print(tweet_data)
    tweet_data['id'] = tweet.id
    tweet_data['id_str'] = tweet.id_str
    tweet_data['sentiments'] = sentiments(tweet_data['message'])
    tweet_data['screen_name'] = tweet.user.screen_name
    try:
        if(len(tweet.user.location)>0):
            print("i entered once ")
            location_search = [x.strip() for x in tweet.user.location.split(',')]
            places = api.geo_search(query=location_search[0], granularity="city")
            print("helo ")
            if(len(places) == 0):
                print("i entered")
                places = api.geo_search(query=location_search[0], granularity="neighborhood")
                for place in places:
                    tweet_data['centroid'] = place.centroid
                    tweet_data['city'] = place.name
                    tweet_data['country'] = place.country
                    tweet_data['state'] = place.name
            else:
                for place in places:
                    tweet_data['centroid'] = place.centroid
                    tweet_data['city'] = place.name
                    tweet_data['country'] = place.country
                    tweet_data['state'] = place.contained_within[0].name

    except ValueError:
        continue
    except IndexError:
        continue
    try:
        if(tweet_data['country'] and tweet_data['country'] != 'India'):
    
            continue
        tweet_data['state'] = state_code[tweet_data['state']]
    except KeyError:
        tweet_data['state'] = None
        r = requests.post('http://localhost:5000/tweets/store', json={"tweet": tweet_data})
        continue
    
    r = requests.post('http://localhost:5000/tweets/store', json={"tweet": tweet_data})
    print(r.text)
    
   

print(tweetResponse)
