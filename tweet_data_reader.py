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


Python Tweet Data Reader: This is an example of how to use and process stored tweets. 

This module can be called externally to load the data into RAM for further processing.

To test the script, run the example bellow from commandline. It will read an archive and display tweets.

Usage:
    python tweet_streamer.py <datafolder_path> 
"""

import os
import sys
import json
import gzip


def get_file_names(data_dir):
    """
    Reads file names in a give directory and returns is a list

    Args:
        data_dir - str: a path to a folder with tweets

    Returns:
        file_list - list: a list of strings
    """
    return [file_name for file_name in os.listdir(data_dir) if file_name.endswith(".pkl")]


def load_twitter_dict(path):
    """
    Loading archived cPickled dict
    Note: this function here is for the reference
    
    Args:
        path - str: path to cPickle 
    
    Returns:
        tweet_list - list: list of json files
    """
    with gzip.open(path, 'rb') as f:
        tweet_list = f.readlines()
    return tweet_list


def read_tweets(tweet_list):
    """
    Decodes text string into Json (dict) objects and prints the content of "text" field.

    Args:
        tweet_list - list: list of json strings

    """
    for line in tweet_list:
        try:
            j = json.loads(line.strip())
            print j['text']
        except:
            pass  # some tweets are malformed - we ignore them


def main(data_dir):
    """
    Main function
    """
    # reading the data
    file_list = get_file_names(data_dir)
    if len(file_list) == 0:
        print 'The directory "%s" is empty. Make sure you point to the correct folder.' % data_dir
        exit(1)
    
    # loading an archive
    print "\nArchive name: %s \n" % file_list[0]
    tweet_list = load_twitter_dict(data_dir + file_list[0])

    # extracting tweet text field
    read_tweets(tweet_list)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print __doc__
    else:
        main(sys.argv[1])
