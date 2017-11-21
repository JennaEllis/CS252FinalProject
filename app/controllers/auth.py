import binascii
import os
from flask import jsonify
from app import app, db
from app.models.user import User, Role
from flask import Blueprint, request
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import hash_password, verify_password

auth = Blueprint('auth', __name__)


# Setup for Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


def validate_request(request):
    """Validates a http request"""
    data = request.get_json()

    email = data['email']
    token = data['token']

    user = User.query.filter_by(email=email).first()

    if user is None:
        return False

    if user.token != token:
        return False

    return True


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
        response['message'] = f'{email} was added'
        code = 201
    except Exception as e:
        response['status'] = 'failure'
        response['message'] = 'An account is already using this email.'
        response['error'] = str(e)
        code = 404

    return jsonify(response), code


@auth.route('/login', methods=['POST'])
def login():
    """Creates a session for the current user"""
    data = request.get_json()

    email = data['email']
    password = data['password']

    response = dict()
    code = 400

    try:
        user = User.query.filter_by(email=email).first()

        if verify_password(password, user.password):
            user.token = binascii.b2a_hex(os.urandom(16))
            db.session.commit()

            response['email'] = user.email
            response['name'] = user.name
            response['token'] = user.token
            response['status'] = 'success'
            response['message'] = 'user successfully logged in'
            code = 202
        else:
            response['status']: 'failure'
            response['message']: 'invalid email or password'
            code = 401
    except Exception as e:
        response['error'] = str(e)

    return jsonify(response), code


@auth.route('/logout', methods=['POST'])
def logout():
    """Deletes the current user's session"""
    response = dict()

    if not validate_request(request):
        response['status'] = 'failure'
        response['message'] = 'invalid request'
        code = 401
        return jsonify(response), code

    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        user.token = "0"
        db.session.commit()

        response['status'] = 'success'
        response['message'] = f'logged out user'
        code = 200
    except Exception as e:
        response['status'] = 'failure'
        response['message'] = f'could not log out user'
        response['error'] = str(e)
        code = 400

    return jsonify(response), code
