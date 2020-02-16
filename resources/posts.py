import models 

from flask import Blueprint, jsonify, request

posts = Blueprint('posts', 'posts')


@posts.route('/')
def test_route():
	return 'check terminal'