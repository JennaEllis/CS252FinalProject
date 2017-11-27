import binascii
import os

from app import app, db
from app.models.user import User, Role

from flask import Blueprint, jsonify, request
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import hash_password, verify_password

auth = Blueprint('auth', __name__)


# Setup for Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


def validate_request(req):
    """Validates an http request"""
    data = req.get_json()

    email = data['email']
    token = hash_password(data['token'])

    user = User.query.filter_by(email=email).first()

    if user is None or not verify_password(user.token, token) or token == "0":
        return None

    return user


@auth.route('/signup', methods=['POST'])
def signup():
    """Adds a new user to the database"""
    data = request.get_json()

    email = data['email']
    name = data['name']
    password = hash_password(data['password'])
    token = "0"

    response = dict()

    try:
        db.session.add(User(email=email, name=name, password=password, token=token))
        db.session.commit()

        response['status'] = 'success'
        response['message'] = f'Created a new account with email: {email}'
        response['code'] = 201
    except Exception as e:
        response['status'] = 'failure'
        response['message'] = 'An account is already using this email.'
        response['error'] = str(e)
        response['code'] = 404

    return jsonify(response)


@auth.route('/login', methods=['POST'])
def login():
    """Creates a session for the current user"""
    data = request.get_json()

    email = data['email']
    password = data['password']

    response = dict()

    user = User.query.filter_by(email=email).first()

    if user is not None and verify_password(password, user.password):
        user.token = hash_password(binascii.b2a_hex(os.urandom(16)))
        db.session.commit()

        response['email'] = user.email
        response['name'] = user.name
        response['token'] = user.token

        response['status'] = 'success'
        response['message'] = f'{user.name} successfully logged in.'
        response['code'] = 202
    else:
        response['status'] = 'failure'
        response['message'] = 'Invalid email or password given.'
        response['code'] = 401

    return jsonify(response)


@auth.route('/logout', methods=['POST'])
def logout():
    """Deletes the current user's session"""
    response = dict()

    if not validate_request(request):
        response['status'] = 'failure'
        response['message'] = 'Received invalid request.'
        response['code'] = 401
        return jsonify(response)

    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user is None:
        response['status'] = 'failure'
        response['message'] = 'Could not logout.'
        response['code'] = 400
    else:
        user.token = "0"
        db.session.commit()

        response['status'] = 'success'
        response['message'] = 'Successfully logged out.'
        response['code'] = 200

    return jsonify(response)
