#!/usr/bin/env python
from flask import Flask
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for
from flaskext.cache import Cache

from redditorstats import get_percentages

app = Flask(__name__)
app.config.from_pyfile('web.cfg')
cache = Cache(app)

@cache.memoize(timeout=86400)
def get_stats(username):
    return get_percentages(username)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('stats', username=request.form['username']))

    return render_template('index.html')

@app.route("/<username>")
def stats(username):
    data, total = get_stats(username)
    return render_template('stats.html', username=username, data=data, total=total)

if __name__== "__main__":
    app.run(debug=True)
    url_for('static', filename='style.css')
    url_for('static', filename='favicon.ico')
