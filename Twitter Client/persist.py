def load_user_info():

    ''' Deserailize and return the user info object'''

    try:
        i = pickle.load(open(config.user_info, "rb"))
        logging.debug( "loaded user_info file {}".format(config.user_info) )
    except Exception as e:
        logging.critical(
            "failed loading user_info from {}: {}".format(config.user_info, e)
        )
        exit(1)

    return i

def dump_user_info(user_info):

    ''' Serialize and write to disk the user info object '''

    try:
        pickle.dump(user_info, open(config.user_info, "wb"))
    except Exception as e:
        logging.critical(
            "failed dumping user_info to {}: {}".format(config.user_info, e)
        )
        exit(1)

def generate_user_entry(screen_name):

    ''' return an object to be added to the user info dict '''

    logging.debug("generating new user entry for {}".format(uid))

    return {
        "screen_name": screen_name,
        "bypass_filters" : False,
        "permaban" : False,
        "next_post_allowed" : "",
        "accepted_tweets" : [],
        "rejected tweets" : [],
        "throttle_factor" : 1
    }