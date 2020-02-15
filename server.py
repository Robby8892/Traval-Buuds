from flask import Flask

import models

DEBUGGER = True
PORT = 8000



app = Flask(__name__)


@app.route('/')
def test_route():
	return 'Hello World'



if __name__ =='__main__':
	models.switch_on_db()
	app.run(debug=DEBUGGER, port=PORT)




