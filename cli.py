#!/usr/bin/env python
import sys
from redditorstats import get_percentages

def main(username):
    data, total = get_percentages(username)

    f = '{0:30} {1}'
    print(f.format('Subreddit', 'Activity'))
    print("--------------------------------------------")

    for subreddit in data:
        percent = "%.2f" % subreddit[1];
        print(f.format(subreddit[0], percent))

    print('--------------------------------------------')
    print(f.format('TOTAL', total))

def prompt_username():
    username = raw_input('What user would you like to look up?\n')
    main(username)

if __name__== "__main__":
    if len(sys.argv) < 2:
        prompt_username()
    else:
        main(sys.argv[1])

