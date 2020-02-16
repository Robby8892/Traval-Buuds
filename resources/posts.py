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
def logged_in_posts_index():


	current_user_posts = [model_to_dict(post) for post in current_user.posts]


	for post in current_user_posts:
		post['photo'] = post['photo'].decode('utf8').replace("",'')
		print('_' * 20)
		post['user'].pop('password')


	return jsonify(
		data=current_user_posts,
		message=f'You have retrived all posts by {current_user.email}, there is a total of {len(current_user_posts)}',
		status=200
		), 200

@posts.route('/other_users', methods=['GET'])
def other_users_posts():

	posts = models.Post.select().where(models.Post.user_id != current_user.id).dicts()

	post_dicts = []

	for post in posts:
		post['photo'] = post['photo'].decode('utf8').replace("",'')
		print('_' * 20)

		post_dicts.append(post)

	return jsonify(
		data=post_dicts,
		message='Here is a list of all of , posts ',
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

# delete route for posts
@posts.route('/<id>', methods=['Delete'])
@login_required
def delete_post(id):

	post_to_delete = models.Post.get_by_id(id)


	try: 
		if current_user.id == post_to_delete.user.id:
			post_to_delete.delete_instance()

			return jsonify(
				data={},
				message='You have deleted post id # {}'.format(post_to_delete.id),
				status=200
				), 200

		else:	
			return jsonify(
				data={
				'error': 'Forbidden'
				},
				message='You are not allowed to delete this post',
				status=403,
				), 403
				

	except models.DoesNotExist:	
		
		return jsonify(
			data={
			'error': 'Forbidden'
			},
			message='You are not allowed to delete this post',
			status=403,
			), 403
