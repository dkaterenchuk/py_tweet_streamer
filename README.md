# py_tweet_streamer
# Twitter streaming library based on tweepy api  

Python twitter streamer is a script that searches and downloads tweets in the real time (limited to 1 request/3s).
The tweets are stored as a gzip compressed text file with json inside. The script stores the
data in chunks of one day. This is done to clear the RAM and optimize the portability of the data.

#### Important
In order for this script to work, you need to add your credentials to the TOKENS.txt file. (Use TOKENS.txt.example as
your reference)

This script is designed to run to without interruption for extended period of time. All data is stored in a given
folder. It is also fail tolerant. In order to stop the script, press "ctrl+c" twice or simply kill the process.

### Installation
Download or clone the package and follow the usage instructions to run it.

### Requirements
Before using this scrip, follow the guidelines defined on Twitter site to obtain Tokens. They are authorization keys
to streaming Twitter API. Follow these guidelines: https://dev.twitter.com/oauth/overview/application-owner-access-tokens

After the step above, add the tokens to local TOKENS.txt file (use TOKENS.txt.example as a reference). Make sure to
keep this file secured and do not publish it anywhere. You might want to use "chmod -400 TOKENS.txt" if you are on
Linux system. It will limit access to the file.

### Dependencies
* Tweepy -  https://github.com/tweepy/tweepy
	`pip install tweepy`
	 
### Usage

```python
    $ python tweet_streamer.py <output_datafolder_path> <search_phrase1> [search_phrase2] [search_..n]
```
where:
output_datafolder_path - path to a directory where the data will be stored
search_phrase - a phrase or a sequence of phrases that will be used to search and retrieve tweets.


For example: in order to stream all news tweets related to the election in the USA, use the following command.
```python
    $ python tweet_streamer.py my_data/ news usa election 
```

### Data
The data is stored in zipped gzip files. Each file contains one day of streaming. This approach will make data
management much easier. The tweets itself are in json string representation (python dictionary). They are unaltered and contain information such as location, re-tweets, etc. An example of reading and working with the data can be
found in tweet_data_reader.py

### License

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
