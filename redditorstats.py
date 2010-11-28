import urllib
import json
import time
from collections import defaultdict

def get_all_stats(username):
    comments = get_stats(username, 'comments')
    submitted = get_stats(username, 'submitted')
    data = dict(comments) 
    data.update(submitted)
    return data

def get_stats(username, api, last_fetch=None, after=None):
    """ api should be comments or submitted """
    subreddits = defaultdict(int)
    url = 'http://www.reddit.com/user/%s/%s.json?count=100' % ( username, api)

    if after:
        url += '&after=%s' % ( after )

    if last_fetch:
        delta = time.time() - last_fetch

        # reddit requires us to wait 3 seconds per request
        if (delta < 3):
            time.sleep((3 - delta))

    json_data = json.loads(urllib.urlopen(url).read())

    last_fetch = time.time() 

    for item in json_data['data']['children']:
        subreddit = item['data']['subreddit']
        subreddits[subreddit] += 1
    
    if (json_data['data']['after'] != None):
        new_subreddits = get_stats(username, api, last_fetch=last_fetch, after=json_data['data']['after'])
        for k, v in new_subreddits.iteritems():
            subreddits[k] += v

    return subreddits


def get_percentages(username):
    subreddits = get_all_stats(username)

    total = sum(subreddits.values())

    percents = {}

    for subreddit in subreddits:
        hits = subreddits[subreddit]
        percents[subreddit] = round((float(subreddits[subreddit])/total * 100), 2)

    return (sorted(percents.items(), key=lambda t: t[1], reverse=True), total)
