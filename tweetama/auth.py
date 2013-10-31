from tweetama import app
from flask import Flask, session, url_for, render_template, request, redirect
import flask.ext.login
from flask_oauth import OAuth
from models import db, User
import twitter

oauth = OAuth()

# Set up twitter OAuth client
twitter = oauth.remote_app('twitter',
    base_url          = 'https://api.twitter.com/1/',
    request_token_url = 'https://api.twitter.com/oauth/request_token',
    access_token_url  = 'https://api.twitter.com/oauth/access_token',
    authorize_url     = 'https://api.twitter.com/oauth/authenticate',
    consumer_key      = 'hBEsh60nTJqhrhB6447AxA',
    consumer_secret   = 'BAILvVEQo7DhQkE66YaLSnzY0eJ0heUlsOF5XdVk'
)

# returns a tuple of twitter tokens, if they exist
@twitter.tokengetter
def get_twitter_token(token=None):
	return session.get('twitter_token')

@app.route('/login')
def login():
	return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next'), _external=True))

@app.route('/oauth_authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
	next_url = request.args.get('next') or url_for('index')
	if resp is None:
		return "Error Occured."
	#check if username exists in db:
	check = User.query.filter_by(username=resp['screen_name']).first()
	if check is None:
		newUser = User(resp['screen_name'], resp['oauth_token'], resp['oauth_token_secret'])
		db.session.add(newUser)
		db.session.commit()
	session['loggedin'] = True
	session['token'] = resp['oauth_token']
	session['username'] = resp['screen_name']
	return redirect("/dash")