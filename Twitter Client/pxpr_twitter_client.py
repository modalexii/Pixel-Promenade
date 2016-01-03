#! python3

def fetch_tweets():

    '''
    Pull tweets with the requisite mention and hashtag from Twitter. 
    Return dict of raw API data.
    '''

    sys.path.append( "{}/lib/requests-oauthlib".format(script_dir) )
    sys.path.append( "{}/lib/TwitterSearch".format(script_dir) )

    import TwitterSearch

    try:
        # Docs: https://github.com/ckoepp/TwitterSearch/blob/master/docs/advanced_usage_tso.rst
        tso = TwitterSearch.TwitterSearchOrder() 
        #tso.set_locale('en') # en locale to avoid odd chars, != language
        #tso.set_keywords(["@PixelPromenade", "#DisplayText"])
        tso.set_keywords([config.handle, config.hashtag])
        tso.set_positive_attitude_filter() # this may quietly block a lot of content
        tso.set_result_type('recent')
        tso.set_count(5) # API max = 100
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

    logging.debug(
        "fetched {} tweets" .format(len(tso))
    )

    return ts.search_tweets_iterable(tso)


def main():

    import sys, os, datetime, logging, pickle

    script_dir = os.path.dirname( os.path.realpath(__file__) )
    sys.path.append( script_dir )
    
    import config, persist, filters

    logging.basicConfig(
        filename = config.run_log, 
        format = config.log_format, 
        level = logging.DEBUG
    )

    logging.info("Begin execution")

    users = persist.load_user_info()
    tweets = fetch_tweets()
    tweets = filters.run_tests(tweets, users)

    from pprint import pprint

    for t in tweets:
        pprint( t)#"@%s tweeted: %s" % (
            #t["user"]["screen_name"],
            #t["text"]
            #)
        #)
        print("------------------------------\n\n")

    logging.info("End execution")


if __name__ == "__main__":
    main()