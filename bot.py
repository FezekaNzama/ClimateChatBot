import tweepy
import sched, time
from datetime import date


consumer_key = 'OqoJiQnStIwODsKXCMOR93g3v'
api_secret = '9jhSSSGwG8eHVFslZWh8gQfdUo7b9EEJnwOh1Sn5reDqDzzKxk'
access_token = '1494806422046973953-5tbXgWBuHeRtwB1rURhQ8UusxwlnwP'
access_token_secret = '3yPet06s9zcdxHpFinHTuvxdn9lHysjkrfB0TfPvVgDmI'

auth = tweepy.OAuthHandler(consumer_key,api_secret)
auth.set_access_token(access_token,access_token_secret )
api = tweepy.API(auth)

#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print(tweet.text)

tweet_ids = []
tweet_per_run = 20
account_followed = []

#function to find and follow verified news accounts
def follow_news():
    query =f"news filter:verified"
    list_outlets = api.search_users(q=query, page=5, count=500, include_entities=False)
    #print(list_outlets[0])
    for outlet in list_outlets:
        #print(outlet.screen_name)
        if outlet.screen_name not in account_followed:
            api.create_friendship(screen_name=outlet.screen_name)
            account_followed.append(outlet.screen_name)

#function to retweet environmental news
def retweet_news():
    query = f'"climate change" OR #climatechange OR #climate OR #environment -filter:retweets filter:verified'
    for tweet in tweepy.Cursor(api.search_tweets, q=query, lang='en', count=100).items(1):
      api.retweet(id=tweet.id)  

def attempt():
    print('Running.')

s = sched.scheduler(time.time, time.sleep)

while True:
    s.enter(86400, 1, retweet_news)
    s.run()