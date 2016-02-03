import sys, os, logging

script_dir = os.path.dirname( os.path.realpath(__file__) )
sys.path.append( script_dir )

import config

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
        t["text"].decode("cp1252")
    except UnicodeEncodeError:
        return True


def user_rate_limited(users, uid):

    '''
    Given user ID, return True if current time is before next_post_allowed
    '''

    from datetime import datetime

    n = users[uid]["next_post_allowed"]

    try:
        n = datetime.strptime(n, "%X %x")
    except ValueError:
        pass
    else:
        if n < datetime.now():
            return True

    


'''
def display_rate_limited():
    PLACE HOLDER. DECIDE HOW TO QUANTIFY THIS.

'''

def run_tests(tweets, users):

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

        # Get user info, or create a new entry if this user is not in our
        # records

        try:

            users[uid]
            logging.debug("processing tweet {} from known user {}".format(uid, sn))

            if users[uid][bypass_filters]:
                continue

        except KeyError:

            logging.debug("processing tweet {} from new user {}".format(uid, sn ))
            users[uid] = persist.generate_user_entry(sn)

        if is_retweet(t):
            logging.info("Reject retweet https://twitter.com/statuses/{} from @{}".format(uid, sn))
            reject_tweets.append(t)
            continue

        if has_url(t):
            logging.info("Reject hyperlink https://twitter.com/statuses/{} from @{}".format(uid, sn))
            reject_tweets.append(t)
            continue

        if has_media(t):
            logging.info("Reject media https://twitter.com/statuses/{} from @{}".format(uid, sn))
            reject_tweets.append(t)
            continue

        if has_financial_symbols(t):
            logging.info("Reject tickersymbol https://twitter.com/statuses/{} from @{}".format(uid, sn))
            reject_tweets.append(t)
            continue

        if has_blacklisted_words(t):
            logging.info("Reject badword https://twitter.com/statuses/{} from @{}".format(uid, sn))
            reject_tweets.append(t)
            continue

        if has_unsupported_chars(t):
            logging.info("Reject badchar https://twitter.com/statuses/{} from @{}".format(uid, sn))
            reject_tweets.append(t)
            continue

        if user_rate_limited(users, uid):
            logging.info("Reject limiteduser @{}".format(uid))
            reject_tweets.append(t)
            continue

        # If t made it this far, it is ok to  display. Add it to list of items
        # to return.
        acceptable_tweets.append(t)

    # display_over_marquee_limit(t)

    return (acceptable_tweets, reject_tweets)


