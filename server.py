from flask import Flask

import models

from resources.users import users

DEBUGGER = True
PORT = 8000



app = Flask(__name__)


# user route imported from resources 

app.register_blueprint(users, url_prefix='/api/v1/users')


@app.route('/')
def test_route():
	return 'Hello World'



if __name__ =='__main__':
	models.switch_on_db()
	app.run(debug=DEBUGGER, port=PORT)




