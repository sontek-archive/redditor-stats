#!/usr/bin/env python
from flask import Flask
from flask import render_template, url_for
from redditorstats import get_percentages

app = Flask(__name__)

@app.route("/<username>")
def stats(username):
    data, total = get_percentages(username)
    return render_template('stats.html', username=username, data=data, total=total)

if __name__== "__main__":
    app.run(debug=True)
    url_for('static', filename='style.css')
    url_for('static', filename='favicon.ico')
