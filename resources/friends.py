import models

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict


friends = Blueprint('friends', 'friends')



# this is where the request will be sent
# I need to send it and update the status to pending 
# when it is sent the user who I sent it to must be able to 
# see it and be able to responsd to it 
@friends.route('/<id>', methods=['POST'])
@login_required	
def create_friend(id):
	
	friend = models.User.get_by_id(id)

	new_friend = models.Friend.create(
		username=current_user.id,
		my_friends=friend,
		status_of_request='pending'
		)

	new_friend_dict = model_to_dict(new_friend)

	new_friend_dict['username'].pop('password')
	new_friend_dict['my_friends'].pop('password')

	print(new_friend)
	print('Here is my new friend')
	print(new_friend_dict['my_friends']['id'])


	return jsonify(
		data=new_friend_dict,
		message='Congrats you have a new friend request sent to {}'.format(new_friend_dict['my_friends']['username']),
		status=200
		), 200

# see all of my friends
@friends.route('/', methods=['GET'])
@login_required
def get_my_friends():

	my_friends_dict = [model_to_dict(friend) for friend in current_user.my_friends]

	for friend in my_friends_dict:
		friend['username'].pop('password')
		friend['my_friends'].pop('password')
		print(friend['my_friends'])



	return jsonify(
		data=my_friends_dict,
		message='Here is a list of all your friends{}'.format(my_friends_dict),
		status=200
		), 200


# remove a friend from your friend list
@friends.route('/<id>', methods=['Delete'])
@login_required
def remove_friend(id):
	
	friend_to_delete = models.Friend.get_by_id(id)

	try:
		if friend_to_delete.username.id == current_user.id:
			friend_to_delete.delete_instance()

			return jsonify(
				data={},
				message='You have removed a friend from your list, id # {}'.format(friend_to_delete.my_friends.id),
				status=200
				), 200

		else: 
			return jsonify(
				data={
				'error': 'forbidden'
				},
				message='You are not allowed to remove this user as they are not in your friend list',
				status=401
				), 401	
	except models.DoesNotExist:
			return jsonify(
				data={
				'error': 'forbidden'
				},
				message='You are not allowed to remove this user as they are not in your friend list',
				status=401
				), 401	


@friends.route('friend_request/<id>', methods=['PUT', 'GET'])
@login_required
def manage_friend_request(id):
	payload = request.get

	if request.method == 'GET':

		get_all_requests = [model_to_dict(request) for request in models.Friend.select()]
		
		print(get_all_requests[0]['my_friends'])

		my_requests_list = []

		for my_request in get_all_requests:
			my_request['my_friends'].pop('password')
			my_request['username'].pop('password')
			if my_request['my_friends']['id'] == current_user.id and my_request['status_of_request'] == 'pending':
				my_requests_list.append(my_request)
				
			
				return jsonify(
					data=my_requests_list,
					message='Here is a list of pending friend requests {}'.format(my_requests_list),
					status=200
					), 200
			else:
				return jsonify(
					data={},
					message='You currently have no pending friend requests',
					status=200
					), 200	


	else:

		get_all_requests = [model_to_dict(request) for request in models.Friend.select()]



		return 'update_friend_request'