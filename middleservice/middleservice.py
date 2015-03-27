#!flask/bin/python

"""Alternative version of the ToDo RESTful server implemented using the
Flask-RESTful extension."""

from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
import os
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from keystoneapi import *

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_url_path="")
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'middleservice.db')
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    #id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50))
    activated = db.Column(db.Boolean)

    def __init__(self, uid, username, password, email=None, activated=False):
    	self.id = uid
        self.username = username
        self.password = password
        self.email = email
        self.activated = activated


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserController(object):
	def __init__(self):
		pass

	@staticmethod
	def create_user(user):
		print user
		if user['username'] is None or user['password'] is None:
			return { "Error": "Username or password is empty" }

		# Connect to keystone.
		try:
			uks = create_user(user['username'], user['password'])
		except Exception as e:
			return {"Error": "User already user"}

		if user['email'] is None:
			u = User(uks.id, user['username'], user['password'])	
		u = User(uks.id, user['username'], user['password'], user['email'])
		#u = User(user['username'], user['password'], user['email'])
		db.session.add(u)
		try:
			db.session.commit()
		except IntegrityError:
			return { "Create User error": "Something is duplicate" }
		except Exception as e:
			return {"Error": "User already user"}

		return {"id": uks.id}
	@staticmethod
	def delete_user(id):
		u = User.query.get(id)
		if u is None:
			return {"Error": "No user record"}
		db.session.delete(u)
		try:
			db.session.commit()
		except Exception as e:
			return {"Error: e"}
	@staticmethod
	def update_user(user):
		u = User.query.get(user['id'])
		if u is None:
			return {"Error": "No user record"}
		u.username = user['username']
		u.password = user['password']
		u.email = user['email']

		try:
			db.session.commit()
		except Exception as e:
			return {"Error: e"}
	@staticmethod
	def activate_user(uid):
		u = User.query.get(uid)
		if u is None:
			return {"Error": "No user record"}
		u.activated = True
		# Connect to keystone
		enable_user(uid)
		try:
			db.session.commit()
		except Exception as e:
			return {"Error": e}
		return {"User activated status ": "Success"}

class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                   help='No user provided',
                                   location='json')
        self.reqparse.add_argument('password', type=str, required=True,
        							help='Error password',
                                   location='json')
        self.reqparse.add_argument('email', type=str, default="",
        							help='Error email',
                                   location='json')

        super(UserAPI, self).__init__()

    def post(self):
    	args = self.reqparse.parse_args()
    	user = {'username': args['username'], 'password': args['password'], 'email': args['email']}
    	return UserController.create_user(user)
    def put(self, id):
    	return UserController.activate_user(id)



api.add_resource(UserAPI, '/keystone/api/v1.0/users', endpoint='users')
#curl -i -H "Content-Type: application/json" -X POST -d '{"username":"testuser", "password":"hihihi"}' http://localhost:9899/keystone/api/v1.0/users
api.add_resource(UserAPI, '/keystone/api/v1.0/users/<string:id>', endpoint='user')
#curl -i -H "Content-Type: application/json" -X PUT http://localhost:9899/keystone/api/v1.0/users/3

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=8899, debug=True)

