#!/usr/bin/env python
# 
"""
MIT License

Copyright (c) 2017 Denys Katerenchuk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



Python tweet streamer: Searches and downloads tweets in the real time (limited to 1 request/2seconds). The tweets are
stored as a dictionary of dictionaries using compressed gzip library standard. The tweets are stored in a separate
archive each day. This is done to clear the RAM and optimize the portability of the data. See README for more details.

In order for this script to work, you need to add your credentials to the TOKENS.txt file. (Use TOKENS.txt.example as
your reference) See README for more details.

This script is designed to run to without interruption for extended period of time. All the data is stored in a given
folder. It is also fail tolerant. In order to stop the script, press "ctrl+c" twise or simply kill the process.


Usage:
    python tweet_streamer.py <output_datafolder_path> <search_phrase1> [search_phrase2] [search_..n]

Ex: in order to stream all news tweets related to the election in the USA, use the following command.
    $ python tweet_streamer.py my_data/ news usa election
"""

import os
import sys
import datetime
import tweepy
import time
import json
import gzip


def init_api():
    """
    Initializes tweepy api with local credentials by
    reading local TOKENS.txt file with the following tokens:
    consumer_key=
    consumer_secret=
    access_token=
    access_token_secret=

    Note1: make sure the tokes are in the same order.
    Note2: make sure to limit read/write write only to your user.
    Note3: DO NOT push this file back to public Git
    """
    with open("TOKENS.txt", "r") as f:
        print "Loading tokens..."
        tokens = [t.strip().split("=")[1] for t in f.readlines()]
        auth = tweepy.OAuthHandler(tokens[0], tokens[1])
        auth.set_access_token(tokens[2], tokens[3])
        return tweepy.API(auth), auth    


class CustomStreamListener(tweepy.StreamListener):
    """
    Custom stream listener - a modified/combined version of multiple online tutorials 
    """
    def on_data(self, data):
        self.save_tweet(data)
        time.sleep(3)  # request frequency
        return True

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True

    def save_tweet(self, tweet_json_string):
        """
        Saving json tweets by appending to a file.
        """
        s_time = datetime.date.today().strftime("%Y-%m-%d")
        j_tweet = json.loads(tweet_json_string)
        print s_time
        print j_tweet["text"]        
        with gzip.open(PATH + "/" + s_time + ".pkl", "a") as f:
            json.dump(j_tweet, f)
            f.write(os.linesep)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
    else:
        PATH = sys.argv[1]
        search_phrases = []
        if len(sys.argv) > 2:
            search_phrases = sys.argv[2:]
        while True:
            try:
                api, auth = init_api()
                sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
                sapi.filter(track=search_phrases, languages=["en"])
            except BaseException, e:
                print "Error: {0}".format(e.args)
                print e
                time.sleep(5)  # in case of error
                continue
