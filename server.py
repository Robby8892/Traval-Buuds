from flask import Flask, g

from flask_login import LoginManager

import models

from resources.users import users

DEBUGGER = True
PORT = 8000



app = Flask(__name__)


app.secret_key = 'herIsakdjaksjdMyskadkasjscreaksljdkasjakey'

login_manager = LoginManager()

login_manager.init_app(app)


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



# user route imported from resources 

app.register_blueprint(users, url_prefix='/api/v1/users')


@app.route('/')
def test_route():
	return 'Hello World'



if __name__ =='__main__':
	models.switch_on_db()
	app.run(debug=DEBUGGER, port=PORT)




