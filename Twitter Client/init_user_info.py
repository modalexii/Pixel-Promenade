#! python3

'''

Create a new user info file, with @modalexii able to bypass filters.

CAUTION
CAUTION - Deletes existing user info file without asking!
CAUTION

'''

import sys, os, pickle

script_dir = os.path.dirname( os.path.realpath(__file__) )
sys.path.append( script_dir )

import config

user_info = {
109121242: {
"screen_name": "modalexii",
"bypass_filters" : True,
"permaban" : False,
"next_post_allowed" : "",
"accepted_tweets" : [],
"rejected tweets" : [],
"throttle_factor" : 1
},
}

pickle.dump(user_info, open(config.user_info, "wb"))