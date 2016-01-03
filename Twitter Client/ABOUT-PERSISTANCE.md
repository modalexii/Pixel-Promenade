# Persistant User Data Storage

This document describes the way in which user data is stored between script executions.

A single object containing all user data is serialized and saved to disk via [pickle](https://docs.python.org/3/library/pickle.html).  The following is stored for each user:

 - Twitter user ID, stored as the key in the `user_info` dict
 - `screen_name` (string) - User screen name
 - `bypass_filters` (boolean) - if True skip all checks (set manually for development & testing)
 - `permaban` (boolean) - Whether or not we permanently prohibit their messages from getting through
 - `next_post_allowed` (datetime) - When they are next allowed to post (enforces rate limiting)
 - `accepted_tweets` (list) - A list of IDs of their tweets that have been accetped
 - `rejected_tweets` (list) - A list of IDs of their tweets that have been rejected
 - A multiplier used when calculating their next
 - `throttle_factor` (int) - A multiplier sometimes used to increase `next_post_allowed` calculations

### Example Object

The pickled object could look like this:

    user_info = {
        432345654: {
            u'screen_name': u'@ScreenNameEg',
            u'bypass_filters' : True,
            u'permaban' : False,
            u'next_post_allowed' : "123123",
            u'accepted_tweets' : [683418747743240193],
            u'rejected tweets' : [678454278853242100, 680185203973032551],
            u'throttle_factor' : 4
        },
    }
    
  ### Location on disk
  File name and location relative to script directory is set by `config.user_info`.