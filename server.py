from flask import Flask

DEBUGGER = True
PORT = 8000



app = Flask(__name__)


@app.route('/')
def test_route():
	return 'Hello World'



if __name__ =='__main__':
	app.run(debug=DEBUGGER, port=PORT)




