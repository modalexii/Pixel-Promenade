# search keyword 1: the handle
handle = "@cnn" # "@PixelPromenade"

# search keyword 2: the hash tag
hashtag = "#isis" # "#DisplayText"

# seconds between subsequent writes to the source file
write_delay = 120

# seconds until the source file is cleared after a write
write_clear_delay = 10

# max number tweets to write before stopping (tweets after this are discarded)
writes_per_execution = 3

# number of tweets to request from Twitter
tweetpullcount = 5

# file that MADRIX uses as ticker source
ticker_source = "/tmp/MADRIXtickersrc.txt"

# file containing persistent data on users.
user_info = "persist/user_info.p"

# file logging runtime events
run_log = "persist/main.log"

# file storing tweets for development functionality
dev_tweets = "persist/dev_tweets.p"

# run_log format
log_format = "%(asctime)s %(levelname)s:%(message)s"

# file containing blacklisted words
blacklist_words_file = "blacklist_words.txt"