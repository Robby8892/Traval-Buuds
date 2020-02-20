import os

# import cloudinary, cloudinary.uploader, cloudinary.api

from flask import Flask, g, jsonify

from flask_cors import CORS

# from werkzeug.utils import secure_filename

from flask_login import LoginManager

import models

from resources.users import users

from resources.posts import posts


os.environ['API_KEY'] = '599414192145716'
os.environ['API_SECRET'] = 'XAWc70FF5oXcrspPBkdSjg9FnQg'
os.environ['ENV_VAR'] = 'CLOUDINARY_URL=cloudinary://599414192145716:XAWc70FF5oXcrspPBkdSjg9FnQg@dyadlealg'

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

CORS(users, origins=['http://localhost:3000', 'https://traval-buuds-react-app.herokuapp.com'], supports_credentials=True)

CORS(posts, origins=['http://localhost:3000', 'https://traval-buuds-react-app.herokuapp.com'], supports_credentials=True)

# user route imported from resources 

app.register_blueprint(users, url_prefix='/api/v1/users')

app.register_blueprint(posts, url_prefix='/api/v1/posts')


# need to come back to cloudinary when I have time
# cloudinary.config(cloud_name='dyadlealg', api_key=os.environ['API_KEY'], api_secret=['API_SECRET'])
# cloudinary.uploader.upload('https://www.pexels.com/photo/adult-siberian-husky-selected-focus-803766/')

# print(cloudinary.uploader)




if 'API_KEY' in os.environ:
	print('Var defined in enviorment')
else:
	print('there is nothing there!')	

@app.route('/')
def test_route():
	return 'Hello World'


if 'ON_HEROKU' in os.environ:
	print('Running on Heroku!')
	models.switch_on_db()


if __name__ =='__main__':
	models.switch_on_db()
	app.run(debug=DEBUGGER, port=PORT)



