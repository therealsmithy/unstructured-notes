# The following is relatively extensible to
# to many API issues that you will encounter. 
# The key is to understand the structure of the data
# that you are getting back and then wrangling that
# json data into a pandas DataFrame.

import pandas as pd
import requests

# The following link was accessed from the Next Gen Stats website
# You have to look into the Network tab of the Developer Tools to find the link

link = 'https://nextgenstats.nfl.com/api/leaders/time/sack?limit=50&season=2024&seasonType=REG'

# For this site, you'll need to include the following headers
# to get the data. You can find the headers in the headers tab
# of the link. Not all sites need the same info, so you'll have
# to trial and error to see what you need.

headers = {
    'Host': 'nextgenstats.nfl.com',
    'Referer': 'https://nextgenstats.nfl.com/stats/top-plays/fastest-sacks/2024/REG/all',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0'
}

# Now, you can just make the request. 

next_gen_req = requests.get(link, headers=headers)

# You'll find that this request returns a JSON object.
# By itself, it isn't useful -- we will want to convert 
# it to a DataFrame

next_gen_data = next_gen_req.json()

# The data is nested, so we'll want to 
# see the key names to determine how to flatten it

next_gen_data.keys()

# The data we want is in the 'leaders' key:

next_gen_data['leaders']

# As you look at it, you'll see that the data is very 
# nested. If you've taken data wrangling, you might
# remember this...

# I want to test out getting a single list element out of 
# the nested data. If I can do it for one, I can do it
# for all. 

next_gen_data['leaders'][0]
next_gen_data['leaders'][0]['leader']

# I'll create 2 data frames, one for the leader and one for the play

df_leader = pd.DataFrame([next_gen_data['leaders'][0]['leader']])

df_play = pd.DataFrame([next_gen_data['leaders'][0]['play']])

# Now, I'll concatenate the two data frames column-wise

pd.concat([df_leader, df_play], axis=1)

# Looks great, so now I can do this for all 
# all the elements

# I'll create an empty list to store the results

next_gen_results = []

# I'll loop through the leaders and plays, creating a data frame for each

for leader in next_gen_data['leaders']:
    # I'll create a data frame for the leader
    df_leader_res = pd.DataFrame([leader['leader']])
    # And the play
    df_play_res = pd.DataFrame([leader['play']])
    # Concatenate them into a single result
    result = pd.concat([df_leader_res, df_play_res], axis=1)
    # And then append that result to the list
    next_gen_results.append(result)

# Finally, I'll concatenate all the results into a single data frame
# By default, it will concatenate row-wise
pd.concat(next_gen_results)

# https://collegescorecard.ed.gov/data/api-documentation/
