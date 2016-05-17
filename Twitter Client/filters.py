#! python3
# -*- coding: utf-8 -*-

import sys, os, logging

script_dir = os.path.dirname( os.path.realpath(__file__) )
sys.path.append( script_dir )

import config, persist

def is_retweet(t):

    '''
    Given a dict representing a tweet, return true if it is a retweet
    '''
    try:
        if(t["retweeted_status"]):
            return True
    except KeyError:
        pass

def has_url(t):

    '''
    Given a dict representing a tweet, return true if the text contains a url
    '''

    try:
        if(t["entities"]["urls"]):
            return True
    except KeyError:
        pass

def has_media(t):

    '''
    Given a dict representing a tweet, return true if it has media attached
    '''

    try:
        if(t["entities"]["media"]):
            return True
    except KeyError:
        pass

def has_financial_symbols(t):

    '''
    Given a dict representing a tweet, return true if it has financial symbols
    '''

    try:
        if(t["entities"]["symbols"]):
            return True
    except KeyError:
        pass

def has_blacklisted_words(t):

    '''
    Given a dict representing a tweet, return true of any word in the text
    appears on our blacklist
    '''

    file_path = "{}/{}".format(script_dir,config.blacklist_words_file)

    with open(file_path) as f:
        blacklist = f.readlines()

    tweet_words = t["text"].split(" ")

    for w in tweet_words:
        if w in blacklist:
            return True

def has_unsupported_chars(t):
    
    '''
    Given a dict representing a tweet, return true if it contains characters
    outside of Windows-1252
    '''
    try:
        t["text"].encode("cp1252")
    except UnicodeEncodeError:
        return True


def user_rate_limited(uid):

    '''
    Given user ID, return True if user is known and less than tweet_delay time
    has passed
    '''

    from datetime import datetime

    config.tweet_delay
    with open (config.user_info, "r") as f:
        user_info = f.readlines()

    now = datetime.now()

    for index, i in enumerate(user_info):
        entry = i.split(" ")
        if entry[0] == uid:
            # user is known
            last_time = datetime.strptime(entry[1], "%c")
            delta = now - last_time
            if delta.seconds < config.tweet_delay:
                # deny
                return True
            else:
                # ok, and update timestamp
                user_info[index] = "{} {}\n".format(uid, now.strftime("%c"))
                with open(config.user_info, "wb") as f:
                    f.write("{}\n".format(user_info))


        # this user was not known - add them to the list
        with open(config.user_info, "a") as f:
            f.write("{} {}\n".format(uid, now.strftime("%c")))


def already_seen(t):

    '''
    Given a dict representing a tweet, return true if we have already seen
    the tweet id
    '''

    with open (config.ids_file, "r") as f:
        id_history = f.readlines()
    if "{}\n".format(t["id"]) in id_history:
        return True
    else:
        # add ID to file
        with open(config.ids_file, "a") as f:
            f.write("{}\n".format(t["id"]))
    

def run_tests(tweets):

    '''
    Given tweets from fetch_tweets(), return lists of those that pass the
    filters and those that do not
    '''
    
    import persist

    logging.debug("starting filter tests")

    acceptable_tweets = []
    reject_tweets = []

    for t in tweets:

        uid = t["user"]["id"]
        sn = t["user"]["screen_name"]

        if has_unsupported_chars(t):
            # keep this at the top or else non-windows chars throw logging error
            import urllib
            encoded_text =  urllib.parse.quote_plus(t["text"])
            logging.info("Reject badchar \"{}\" from @{}".format(encoded_text, sn))
            reject_tweets.append(t)
            continue

        if is_retweet(t):
            logging.info("Reject retweet \"{}\" from @{}".format(t["text"], sn))
            reject_tweets.append(t)
            continue

        if has_url(t):
            logging.info("Reject hyperlink \"{}\" from @{}".format(t["text"], sn))
            reject_tweets.append(t)
            continue

        if has_media(t):
            logging.info("Reject media \"{}\" from @{}".format(t["text"], sn))
            reject_tweets.append(t)
            continue

        if has_financial_symbols(t):
            logging.info("Reject tickersymbol \"{}\" from @{}".format(t["text"], sn))
            reject_tweets.append(t)
            continue

        if has_blacklisted_words(t):
            logging.info("Reject badword \"{}\" from @{}".format(t["text"], sn))
            reject_tweets.append(t)
            continue

        if already_seen(t):
            logging.info("Reject historical \"{}\" from @{}".format(t["text"], sn))
            reject_tweets.append(t)
            continue

        if user_rate_limited(uid):
            logging.info("Reject limiteduser @{} for \"{}\"".format(uid, t["text"]))
            reject_tweets.append(t)
            continue
        
        # If t made it this far, it is ok to  display. Add it to list of items
        # to return.
        acceptable_tweets.append(t)

    # display_over_marquee_limit(t)

    return (acceptable_tweets, reject_tweets)


