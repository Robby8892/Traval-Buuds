from peewee import *

from flask_login import UserMixin

import datetime

DATABASE = SqliteDatabase('posts.sqlite')


# 1. I will setup my user model first to setup logging in
# 2. Posts model will need to be made once routes work
# and then I will drop my database and incorperate users into 
# the post model
# 3. Bonus! Create a comment model and my_friends models after hitting mvp

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField()
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE


def switch_on_db():
	DATABASE.connect()

	DATABASE.create_tables([User], safe=True)		
	print('Connection made to the db and tables created!')


	DATABASE.close()

