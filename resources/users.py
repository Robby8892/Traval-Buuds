import models

from flask import Blueprint 

users = Blueprint('users', 'users')


#here is my test route

@users.route('/')
def test_routes():
	return 'Hello User Test route'