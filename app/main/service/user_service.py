# import the necessary package

import uuid
import os
import datetime
from flask import jsonify
from app.main import db
from app.main import config
from app.main.model.user import User

def save_new_user(data):
    user = User.query.filter_by(username=data['username'], email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            username=data['username'],
            password=data['password'],
            email=data['email'],
            registered_on=datetime.datetime.utcnow(),
            max_connection=data['max_connection'],
            connected=0
        )
        save_changes(new_user)
        base_dir(data['username'])
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'The email address is already used, Please Log in.'
        }
        return response_object, 409
def update_user(username, data):
    # get user informations
    user = get_a_user(username)
    if user:
        if data['email'] is not None:
            user.email = data['email']
        if data['username'] is not None:
            user.username = data['username']
        if data['max_connection'] is not None:
            user.max_connection = data['max_connection']
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': "update successful",
        }
        return response_object, 201

def get_all_users():
    users = User.query.all()
    return users

def get_a_user(username):
    return User.query.filter_by(username=username).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def base_dir(username):
    """create base directory for the user"""
    if not os.path.isdir(config.BASE_DATA_DIR):
        ">> create base data directory {}...".format(config.BASE_DATA_DIR)
        os.mkdir(config.BASE_DATA_DIR)
    if not os.path.isdir(config.PROCESS_DATA_DIR):
        ">> create process data directory {}...".format(config.PROCESS_DATA_DIR)
        os.mkdir(config.PROCESS_DATA_DIR)
    if not os.path.isdir(config.MODEL_DIR):
        ">> create model directory {}...".format(config.MODEL_DIR)
        os.mkdir(config.MODEL_DIR)
    if not os.path.isdir(os.path.join(config.BASE_DATA_DIR, username)):
        # create data dir
        ">> create base data directory {} ...".format(username)
        os.mkdir(os.path.join(config.BASE_DATA_DIR, username))
    if not os.path.isdir((os.path.join(config.MODEL_DIR, username))):
        # create model dir
        ">> create model directory {} ...".format(username)
        os.mkdir(os.path.join(config.MODEL_DIR, username))
    if not os.path.isdir(os.path.join(config.PROCESS_DATA_DIR, username)):
        # create process data dir
        ">> create process data directory {} ...".format(username)
        os.mkdir(os.path.join(config.PROCESS_DATA_DIR, username))

def generate_token(user):
    try:
        response_object = {
            'status': 'success',
            'message': 'Successfully registered',
            'public_id': user.public_id
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
