#! python3
# -*- coding: utf-8 -*-

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


def build_writeout(tweets):

    '''
    Given tweets from fetch_tweets(), return a list of strings suitable to be
    written to the display
    '''

    import html.parser
    h = html.parser.HTMLParser()

    writeout = []

    '''
    num_tweets = len(tweets)

    if num_tweets > config.writes_per_execution:
        # read from backlog
        with open(persist.backlog, "r") as f:
            backlog = f.readlines()

        for i in config.writes_per_execution - num_tweets:
            try:
                tweets.append(backlog[0])
                backlog = backlog[1:]

        # save backlog file without 

    '''
    for t in tweets:
        text = "@{}: {}".format(t["user"]["screen_name"], t["text"])
        text = h.unescape(text) # replace html entities
        text = text.replace("\n", " ").replace("\r", "")
        writeout.append(text)

    # save excess writeout
    with open(config.backlog, "a") as f:
        f.write("{}\n".format(writeout[config.writes_per_execution:]))

    # return configured number of tweets
    return writeout[:config.writes_per_execution]

def display(writeout):
    
    '''
    Given list of strings from build_writeout(), write each to the ticker
    source file in succession
    '''

    logging.debug("beginning writeout")

    from time import sleep

    for i in writeout:
        logging.info("display \"{}\"".format(i))
        with open(config.ticker_source, 'w') as f:
            f.write(i)
        sleep(config.write_hold)
        logging.debug("clearing ticker source")
        with open(config.ticker_source, 'w') as f:
            f.write("")
        sleep(config.write_delay)


def main():

    unfiltered_tweets = fetch_tweets()

    (accepted_tweets, rejected_tweets) = filters.run_tests(
        unfiltered_tweets,
        #users
    )

    wo = build_writeout(accepted_tweets)
    display(wo)

    logging.info("End execution")
    sys.exit(0)


if __name__ == "__main__":

    import sys, os, datetime, logging, TwitterSearch

    script_dir = os.path.dirname( os.path.realpath(__file__) )
    sys.path.append( script_dir )
    
    import config, persist, filters

    logging.basicConfig(
        filename = config.run_log, 
        format = config.log_format, 
        level = logging.DEBUG
    )

    logging.info("Begin execution")

    main()