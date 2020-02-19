import os

from flask import Flask, g, jsonify

from flask_cors import CORS

# from werkzeug.utils import secure_filename

from flask_login import LoginManager

import models

from resources.users import users

from resources.posts import posts

DEBUGGER = True
PORT = 8000

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'text', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.secret_key = 'herIsakdjaksjdMyskadkasjscreaksljdkasjakey'

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):

	try:
		return models.User.get(models.User.id == user_id)
	except modes.DoesNotExist:	
		return None

@login_manager.unauthorized_handler
def unauthorized():
	return jsonify(
		data={
		'error': 'User is not logged in'

		},
		message='You must be logged in to access that information',
		status=401
		),401


@app.before_request
def before_request():
	"""Will connect to the db before each request"""
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	"""Will disconnect from db after request and return the response"""
	g.db.close()
	return response



# CORS for api calls

CORS(users, origins=['http://localhost:3000'], supports_credentials=True)

CORS(posts, origins=['http://localhost:3000'], supports_credentials=True)

# user route imported from resources 

app.register_blueprint(users, url_prefix='/api/v1/users')

app.register_blueprint(posts, url_prefix='/api/v1/posts')


@app.route('/')
def test_route():
	return 'Hello World'


if 'ON_HEROKU' in os.environ:
	print('Running on Heroku!')
	models.switch_on_db()


if __name__ =='__main__':
	models.switch_on_db()
	app.run(debug=DEBUGGER, port=PORT)




