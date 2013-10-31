import os
from tweetama import app

def runserver():
	port = int(os.environ.get('PORT', 5000))
	app.run(debug = True, host='0.0.0.0')

if __name__ == '__main__':
	runserver()
