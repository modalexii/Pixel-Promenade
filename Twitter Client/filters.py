def is_retweet(t):

    '''
    Given a dict representing a tweet, return true if it is a retweet
    '''

    if(t["retweeted_status"]):
        return True

def has_url(t):

    '''
    Given a dict representing a tweet, return true if the text contains a url
    '''

    if(t["entities"]["urls"]):
        return True

def has_media(t):

    '''
    Given a dict representing a tweet, return true if it has media attached
    '''

    if(t["entities"]["media"]):
        return True

def has_financial_symbols(t):

    '''
    Given a dict representing a tweet, return true if it has financial symbols
    '''

    if(t["entities"]["symbols"]):
        return True

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

'''
Place holder. MADIRX should have full unicode support. If it ends up choking
on certain chars, blacklist those ranges here.

def has_blacklisted_chars(t):
    pass
'''

def run_tests(tweets, users):

    '''
    Given tweets from fetch_tweets(), reject ones that should not be displayed
    for various reasons
    '''

    logging.debug("starting tweet filtering")

    for t in tweets:

        uid = t["user"]["id"]
        sn = t["user"]["screen_name"]

        try:
            user = users[uid]
            logging.debug("processing tweet {} from known user {}".format uid, sn)
            )
        except KeyError:
            logging.debug("processing tweet {} from new user {}".format(uid, sn ))
            user = users[uid] = generate_user_entry(sn)

        if is_retweet(t):
            logging.info("Reject retweet https://twitter.com/statuses/{} from @{}".format(uid, sn))
            continue

        if has_url(t):
            logging.info("Reject hyperlink https://twitter.com/statuses/{} from @{}".format(uid, sn))
            continue

        if has_media(t):
            logging.info("Reject media https://twitter.com/statuses/{} from @{}".format(uid, sn))
            continue

        if has_financial_symbols(t):
            logging.info("Reject tickersymbol https://twitter.com/statuses/{} from @{}".format(uid, sn))
            continue

        if has_blacklisted_words(t):
            logging.info("Reject badword https://twitter.com/statuses/{} from @{}".format(uid, sn))
            continue

        # has_blacklisted_chars(t)`

        # user_over_ratelimit(t)

        # display_over_marquee_limit(t)

        persist.dump_user_info(users)