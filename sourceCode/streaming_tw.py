from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time

import json

consumer_key = "DbFH6f0sMxH7lWZ26WvdGzyfc"
consumer_secret = "rB1ZfJvEjfDGN50i9He7Lg8uBXjjBkfDL42qhN4s3knIsxQkS1"
access_token = "156813469-kDtZ90Mr5TA0AIKhrqLIxCVFX4HuM5e3VBJwc2yD"
access_token_secret = "cT8V9ncpJ8gptZiSxVXgag6bkpNboxjLwmar0JZULSI08"
file_raw = open('../data/Twitter/data_stream_' + time.strftime('%Y%m%d') + '.json', 'w')

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        tweet = json.loads(data)
        if tweet['coordinates']:
            file_raw.write(data)
            print (tweet['text'])
    	# print (tweet['coordinates'])
    	# print ("jnajsj")
        return True

    def on_error(self, status_code):
        if status_code == 429:
            print (status_code)
            print ("Exceed rate limit")
            time.sleep(60*15)
        elif status_code == 420:
            #returning False in on_data disconnects the stream
            print (status_code)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(locations=[-78.573727,-0.260581,-78.395496,-0.065575,])

    # -78.573727,-0.260581,-78.395496,-0.065575  Quito
    # -79.943733,-2.251961,-79.864769,-2.068757 Guayaquil
