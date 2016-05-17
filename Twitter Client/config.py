#! python3
# -*- coding: utf-8 -*-

# search keyword 1: the handle
handle = "@PixelPromenade" # "@PixelPromenade"

# search keyword 2: the hash tag
hashtag = "#letsglow" # "#letsglow"

# seconds between subsequent writes to the source file
write_delay = 60

# seconds to keep text in the source file
write_hold = 100

# max number tweets to write before stopping (tweets after this are discarded)
writes_per_execution = 3

# number of tweets to request from Twitter
tweetpullcount = 50

# number of seconds before a previously seen user has a chance of passing
# filters next
tweet_delay = 15*60

# file that MADRIX uses as ticker source
ticker_source = "C:\\ProgramData\\MADRIX\\ticker_src.txt"

# file containing persistent data on users.
user_info = "persist/user_info.txt"

# file containing backlogged tweets
backlog = "persist/backlog.txt"

# file logging runtime events
run_log = "persist/main.log"

# file storing tweets for development functionality
dev_tweets = "persist/dev_tweets.p"

# file storing tweet IDs
ids_file = "persist/ids.txt"

# run_log format
log_format = "%(asctime)s %(levelname)s:%(message)s"

# file containing blacklisted words
blacklist_words_file = "blacklist_words.txt"