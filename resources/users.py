import models

from flask import Blueprint, jsonify, request 

from flask_bcrypt import generate_password_hash

from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'users')


#here is my test route

@users.route('/')
def test_routes():
	return 'Hello User Test resource'

# register route
@users.route('/register', methods=['POST'])
def register_user():
	payload = request.get_json()

	payload['email'] = payload['email'].lower()
	payload['username'] = payload['username'].lower()

	try:
		models.User.get(models.User.email == payload['email'] or models.User.username == payload['username'] )	

		return jsonify(
			data={},
			message=f'A users with that email already exists',
			status=401
			), 401

	except models.DoesNotExist:

		created_user = models.User.create(
			username=payload['username'],
			email=payload['email'],
			password=generate_password_hash(payload['password'])
			)

		user_dict = model_to_dict(created_user)
		user_dict.pop('password')

		return jsonify(
			data=user_dict,
			message='You have successfully registered {} to the site'.format(user_dict['username']),
			status=201
			), 201