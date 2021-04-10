import os, time
#import cPickle as pickle
import _pickle as pickle
import twython as Twython
#from urllib import *
import urllib.parse
from SETTINGS import *
api = Twython.Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
latest_tweet_id = 0
user_names = ["CoinbaseInsto","binance","BSC_Insider","coinbase","krakenfx"]
for row_id in range(len(user_names)):
        user_name = user_names[row_id]
        print("https://www.twitter.com/"+user_name)
        def first_run():
            file_exists = os.path.exists('sav.p')
            if file_exists is False:
                user_timeline = api.get_user_timeline(screen_name=user_name, count=2)#This 'count' is how many tweets back from the most recent tweet that will be fowarded to telegram
                tweet_id = user_timeline[1]['id']
                file_pickle(tweet_id)
        def get_timeline(latest_tweet_id):
            user_timeline = api.get_user_timeline(screen_name=user_name, since_id=latest_tweet_id)
            return user_timeline
        def read_latest_id():
            line = file_unpickle()
            if len(str(line)) < 2:
                return 0
            else:
                return line
        def send_message(msg):
            #msg = quote(msg, safe='')
            msg = urllib.parse.quote(msg, safe='')
            link = 'https://api.telegram.org/bot'+telegram_token+'/sendMessage?chat_id=@'+channel_name+'\&text="' + msg + '"'
            os.system('curl '+ link)
           
        def file_pickle(var):
            pickle.dump(var, open("sav.p", "wb"))
        def file_unpickle():
            saved = pickle.load(open('sav.p', "rb"))
            return saved
         
        def main():
            latest_tweet_id = read_latest_id()
            user_timeline = get_timeline(latest_tweet_id)
            number_of_tweets = len(user_timeline)
            if number_of_tweets > 0:
                for i in reversed(range(0,number_of_tweets)):
                    if user_timeline[i]['text']:
                        print(user_timeline[i]['text'])
                        send_message(user_timeline[i]['text'])
                        time.sleep(4)
                latest_tweet_id = user_timeline[0]['id']
            file_pickle(latest_tweet_id)
        first_run()
        main()
