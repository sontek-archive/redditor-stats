from flask import Flask
from flask import render_template, url_for
import urllib
import json

app = Flask(__name__)

@app.route("/<username>")
def stats(username):
    subreddits = {};

    urls = ('comments.json', 'submitted.json')
    for url in urls:
        text = urllib.urlopen('http://www.reddit.com/user/%s/%s' % ( username, url )).read()

        if text == '{error: 304}':
            return render_template('error.html')

        for i in json.loads(text)['data']['children']:
            key = i['data']['subreddit']
            if key in subreddits.keys():
                subreddits[key] += 1
            else:
                subreddits[key] = 1

    total = sum(subreddits.values())

    percents = {};

    for subreddit in subreddits:
        hits = subreddits[subreddit];
        percents[subreddit] = round((float(subreddits[subreddit])/total * 100), 2);

    data = sorted(percents.items(), key=lambda t: t[1], reverse=True)
    return render_template('stats.html', username=username, data=data)

if __name__== "__main__":
    app.run(debug=True)
    url_for('static', filename='style.css')
    url_for('static', filename='favicon.ico')
