import models 
import json
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

posts = Blueprint('posts', 'posts')

# create route for posts
@posts.route('/', methods=['POST'])
@login_required
def create_post():
	payload = request.get_json()

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


@posts.route('/', methods=['GET'])
def posts_index():

	current_user_posts = [model_to_dict(post) for post in current_user.posts]

	print(current_user_posts)

	for post in current_user_posts:
		post['photo'] = post['photo'].decode('utf8').replace("",'')
		print('_' * 20)
		post['user'].pop('password')




	return jsonify(
		data=current_user_posts,
		message=f'You have retrived all posts by {current_user.email}, there is a total of {len(current_user_posts)}',
		status=200
		), 200

@posts.route('/<id>', methods=['GET'])
def posts_show(id):
	
	post = models.Post.get_by_id(id)

	if post.user.id == current_user.id:

		post_dict = model_to_dict(post)
		post_dict['photo'] = post_dict['photo'].decode('utf8').replace("",'')
		post_dict['user'].pop('password')

		return jsonify(
		data=post_dict,
		message=f'You have retrived your post id number {id},',
		status=200
		), 200

	else:	

		post_dict = model_to_dict(post)

		post_dict['photo'] = post_dict['photo'].decode('utf8').replace("",'')
		post_dict['user'].pop('password')

		return jsonify(
			data=post_dict,
			message='You have retrived post id number {}, by, {} '.format(id, post_dict['user']['username']),
			status=200
			), 200