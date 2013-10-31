# Put models here

"""
import datetime
from tweetama.core import db

class User(db.DynamicDocument):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	email = db.StringField(max_length=255, required=True, unique=True)

"""
from tweetama import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import datetime

class User(db.Model):
	__tablename__ = 'tweetama'
	uid = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100))
	token = db.Column(db.String(300))
	secret = db.Column(db.String(300))

	def __init__(self, username, token, secret):
		self.username = unicode(username)
		self.token = unicode(token)
		self.secret = unicode(secret)

class AMA(db.Model):
	__tablename__ = 'ama'
	aid = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(300))
	bio = db.Column(db.String(600))
	state = db.Column(db.String(100))

	def __init__(self, username, bio):
		self.username = username
		self.bio = bio