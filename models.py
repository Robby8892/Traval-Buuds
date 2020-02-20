import os

from peewee import *

from flask_login import UserMixin

import datetime

from playhouse.db_url import connect



# 1. I will setup my user model first to setup logging in
# 2. Posts model will need to be made once routes work
# and then I will drop my database and incorperate users into 
# the post model
# 3. Bonus! Create a comment model and my_friends models after hitting mvp


if 'ON_HEROKU' in os.environ:
	DATABASE = connect(os.environ.get('DATABASE_URL'))

else:
	DATABASE = PostgresqlDatabase('posts', user='robertocortes')


class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField()
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE


class Post(Model):
	title = CharField()
	place = CharField()
	photo = CharField(max_length=100000)
	story = CharField()
	created_at = DateTimeField(default=datetime.datetime.now)
	user = ForeignKeyField(User, backref='posts')

	class Meta:
		database = DATABASE

def switch_on_db():
	DATABASE.connect()

	DATABASE.create_tables([User, Post], safe=True)		
	print('Connection made to the db and tables created!')


	DATABASE.close()

