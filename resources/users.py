import models

from flask import Blueprint, jsonify, request 

users = Blueprint('users', 'users')


#here is my test route

@users.route('/')
def test_routes():
	return 'Hello User Test resource'

# register route
@users.route('/register', methods=['POST'])
def register_user():
	payload = request.get_json()

	print(payload)

	return 'check terminal'	