#! python3

import logging, pickle

def load(f):

    '''Wraps pickle.load'''

    try:
        i = pickle.load(open(f, "rb"))
        logging.debug( "loaded file {}".format(f) )
    except Exception as e:
        logging.critical(
            "failed loading from {}: {}".format(f, e)
        )
        exit(1)

    return i

def dump(user_info, f):

    '''Wraps pickle.dump'''

    try:
        pickle.dump(user_info, open(f, "wb"))
    except Exception as e:
        logging.critical(
            "failed dumping user_info to {}: {}".format(f, e)
        )
        exit(1)

def generate_user_entry(screen_name):

    ''' return an object to be added to the user info dict '''

    logging.debug("generating new user entry for {}".format(screen_name))

    return {
        "screen_name": screen_name,
        "bypass_filters" : False,
        "permaban" : False,
        "next_post_allowed" : "",
        "accepted_tweets" : [],
        "rejected tweets" : [],
        "throttle_factor" : 1
    }

'''
user_info = {109121242: {'next_post_allowed': '', 'screen_name': '@modalexii', 'bypass_filters': False, 'throttle_factor': 1, 'permaban': False, 'accepted_tweets': [], 'rejected_tweets': []}}
pickle.dump(user_info, user_info.p)
'''