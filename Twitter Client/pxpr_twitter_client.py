#! python3

def fetch_tweets():

    '''
    Pull tweets with the requisite mention and hashtag from Twitter. 
    Return dict of raw API data.
    '''

    logging.debug("fetching tweets")

    try:
        # Docs: https://github.com/ckoepp/TwitterSearch/blob/master/docs/advanced_usage_tso.rst
        tso = TwitterSearch.TwitterSearchOrder() 
        tso.set_locale("en") # en locale to avoid odd chars, != language
        #tso.set_keywords(["@PixelPromenade", "#DisplayText"])
        tso.set_keywords([config.handle, config.hashtag])
        tso.set_positive_attitude_filter() # this may quietly block a lot of content
        tso.set_result_type("recent")
        tso.set_count(config.tweetpullcount) # API max = 100
        tso.set_include_entities(True) # https://dev.twitter.com/overview/api/entities-in-twitter-objects

        import apikeys

        ts = TwitterSearch.TwitterSearch(
            consumer_key = apikeys.consumer_key,
            consumer_secret = apikeys.consumer_secret,
            access_token = apikeys.access_token,
            access_token_secret = apikeys.access_token_secret,
            verify = True
        )

    except TwitterSearchException as e:
        logging.critical(e)
        exit(1)

    return ts.search_tweets_iterable(tso)

def strip_hashtag(tweets, hashtag):

    '''
    Given tweets from fetch_tweets(), remove the hashtag
    '''

    logging.debug("removing hashtags, object len {}".format(len(tweets)))

    for t,n in enumerate(tweets):

        words = t["text"].split(" ")
        words = words.remove(hashtag)
        t["text"] = " ".join(words)
        tweets[i] = t

    return tweets

def build_writeout(tweets):

    '''
    Given tweets from fetch_tweets(), return a list of strings suitable to be
    written to the display
    '''

    logging.debug("building writeout, object len {}".format(len(tweets)))

    writeout = []

    for t in tweets:
        text = "{}: {}".format(t["users"]["screen_name"], t["text"])
        writeout.append(text)

    return writeout


def update_user_info(users, accepted_tweets, rejected_tweets):

    '''
    Update persistant user data fields
    '''

    logging.debug("updating user info")

    delay = datetime.timedelta(hours=2)
    now = datetime.datetime.now()
    next_base = now + delay

    for t in accepted_tweets:

        uid = t["user"]["id"]

        # reset throttle
        users[uid]["throttle_factor"] = 1

        # set next post time
        n = datetime.datetime.strftime(next_base, "%X %x")
        users[uid]["next_post_allowed"] = n

        # add tweet id to list of accepted tweets
        users[uid][accepted_tweets].append(t["id"])
    

    for t in rejected_tweets:

        uid = t["user"]["id"]

        # if user is new or has been good throttle will be 1 - decrement it to
        # allow them to try again soon. Else, increse throttle.
        if users[uid]["throttle_factor"] == 1:
            users[uid]["throttle_factor"] = .25
        elif users[uid]["throttle_factor"] < 1:
            users[uid]["throttle_factor"] = 1
        else:
            users[uid]["throttle_factor"] += 1

        # set next post time
        n = next_base * users[uid]["throttle_factor"]
        n = datetime.datetime.strftime(n, "%X %x")
        users[uid]["next_post_allowed"] = next_post_allowed

        # add tweet id to list of accepted tweets
        users[uid][rejected_tweets].append(t["id"])

    return users

def writeout_text(writeout):
    
    '''
    Given list of string from build_writeout(), write each to the ticker
    source file in succession
    '''

    logging.debug("beginning writeout")

    from time import sleep

    for i in writeout:
        logging.info("writeout \"{}\"".format(i))
        with open(config.ticker_source, 'w') as f:
            f.write(i)
        sleep(config.write_clear_delay)
        logging.debug("clearing ticker source")
        with open(config.ticker_source, 'w') as f:
            f.write("")
        sleep(config.write_delay)

def save_dev_tweets():

    '''
    Fetch tweets and save the object to disk for use with load_tweets_dev()
    '''

    logging.info("DEVELOPMENT MODE - fetching tweets and writing to disk")

    tweets = fetch_tweets()
    persist.dump(tweets, "{}/{}".format(script_dir, config.dev_tweets))

def load_dev_tweets():

    '''
    Load tweets saved by save_dev_tweets()
    '''

    # using pickle directly is cleaner than using the persist.load() wrapper,
    # which requires importing TwitterSearch and prerequisite actions in
    # persist
    import pickle

    logging.info("DEVELOPMENT MODE - loading tweets from disk")

    tweets = pickle.load(
        open( "{}/{}".format(script_dir, config.dev_tweets, "rb") )
    )

    return tweets

def main():

    logging.debug("args: {}".format(sys.argv[1:]))

    if "{} {}".format(sys.argv[1],sys.argv[2]) == "devmode save":
        save_dev_tweets()
        logging.info("exiting devmode save")
        exit(0)
    elif "{} {}".format(sys.argv[1],sys.argv[2]) == "devmode load":
        unfiltered_tweets = load_dev_tweets()
    elif sys.argv[1]:
        logging.critical("invalid arg {}".format( " ".join(sys.argv[1:])) )
        exit(1)

    users = persist.load( "{}/{}".format(script_dir, config.user_info) )

    if not unfiltered_tweets:
        unfiltered_tweets = fetch_tweets()
        
    (accepted_tweets, rejected_tweets) = filters.run_tests(
        unfiltered_tweets,
        users
    )

    accepted_tweets = strip_hashtag(accepted_tweets, config.hashtag)

    users = update_user_info(users, )
    persist.dump( users, "{}/{}".format(script_dir, config.user_info) )

    wo = build_writeout(accepted_tweets)
    wo = wo[:config.writes_per_execution]
    writeout_text(wo)

    logging.info("End execution")
    exit(0)


if __name__ == "__main__":

    import sys, os, datetime, logging

    script_dir = os.path.dirname( os.path.realpath(__file__) )
    sys.path.append( script_dir )
    sys.path.append( "{}/lib/requests-oauthlib".format(script_dir) )
    sys.path.append( "{}/lib/TwitterSearch".format(script_dir) )
    
    import config, persist, filters, TwitterSearch

    logging.basicConfig(
        filename = config.run_log, 
        format = config.log_format, 
        level = logging.DEBUG
    )

    logging.info("Begin execution")

    main()