import os

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory, session
from models import db, User, AMA

from tweetama import app

# Twitter Auth:
from tweetama import auth

import twitter
#t = twitter.Api(consumer_key='hBEsh60nTJqhrhB6447AxA',
#                      consumer_secret='BAILvVEQo7DhQkE66YaLSnzY0eJ0heUlsOF5XdVk',
#                      access_token_key='240286080-5KHn9fSaHc3CMphTHIg5qg7N1f3mccNX9hvHi7Kg',
#                      access_token_secret='OT7yZ80hHasF2HsVH3Q7jW8BJpPVKRVW5GHt8xot7hUEs')

# app controllers
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

# special file handlers
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')

# error handlers
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.route("/dash")
def dash():
	if not session.get('loggedin'):
		return redirect("/")
	else:
		return render_template("dash.html")

@app.route("/create")
def createAMA():
	if not session.get('loggedin'):
		return redirect("/")
	# check if AMA exists and if it is active or not
	check = AMA.query.filter_by(username=session['username']).first()
	if check is None:
		return render_template("create.html", pageTitle="Create AMA")
	return "wip"

@app.route("/create/sub", methods=['POST'])
def createSub():
	if not session.get('loggedin'):
		return redirect("/")
	userBio = request.form['bio']
	if userBio == "":
		return "All the Fields are Mandatory."
	# check if username exists in AMA db:
	check = AMA.query.filter_by(username=session['username']).first()
	if check is None:
		# create row.
		create = AMA(session['username'], userBio)
		db.session.add(create)
		db.session.commit()
		return redirect("/ama/"+session['username'])
	else:
		return redirect("/ama/"+session['username'])
	return "Error Occured. [create-sub]. Please Report to me@abhishekbiswal.com"

# AMA PAGE:
@app.route("/ama/<username>")
def amaPage(username):
	if username == "":
		return redirect("/Abhishek_Biswal")
	# check if AMA exists.
	check = AMA.query.filter_by(username=username).first()
	if check is None:
		return redirect("/404")
	active = 1
	if check.state != "active":
		return "not active"
		active = 0
	pageTitle = "@"+username+" AMA page on #TweetAMA"
	return render_template("ama.html", pageTitle=pageTitle, username=username, active=active)