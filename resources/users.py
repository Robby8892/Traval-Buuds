import models

from flask import Blueprint, jsonify, request

users = Blueprint('users', 'users')


# register route
users.route('/register', methods=['POST'])
def register_user():
	payload = request.get_json()

	print(payload)

	return 'check terminal'