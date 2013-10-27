from tweetama import app
from models import db

DEBUG = True
SECRET_KEY = '4954caecc75d41da81e22817e8113a520945126ce1b5b5a7'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:abhishekbiswal@localhost/tweetama'
db.init_app(app)