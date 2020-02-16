import models 

from flask import Blueprint, jsonify, request
from flask_login import current_user

from playhouse.shortcuts import model_to_dict

posts = Blueprint('posts', 'posts')


@posts.route('/', methods=['POST'])
def create_post():
	payload = request.get_json()

	print(payload)

	post = models.Post.create(
		title=payload['title'],
		place=payload['place'],
		photo=payload['photo'],
		story=payload['story'],
		user=current_user.id
		)

	post_dict = model_to_dict(post)

	post_dict['user'].pop('password')

	return jsonify(
		data=post_dict,
		message='You have successfully created a new post as {}'.format(post_dict['user']['username']),
		status=201
		), 201
