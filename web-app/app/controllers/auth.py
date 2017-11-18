from app import app, db
from app.models.user import User, Role

from flask import Blueprint, jsonify, request
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security import login_user, login_required, logout_user
from flask_security.utils import hash_password, verify_password

auth = Blueprint('auth', __name__)


# Setup for Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@auth.route('/signup', methods=['POST'])
def signup():
    """Adds a new user to the database"""
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = hash_password(data.get('password'))

    response = dict()

    try:
        db.session.add(User(email=email, username=username, password=password))
        db.session.commit()

        response['status'] = 'success'
        response['message'] = f'{email} was added'
        code = 201
    except Exception as e:
        response['status'] = 'failure'
        response['message'] = f'user already exists'
        response['error'] = str(e)
        code = 404

    return jsonify(response), code


@auth.route('/login', methods=['POST'])
def login():
    """Creates a session for the current user"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    response = dict()

    try:
        user = User.query.filter_by(email=email).first()

        if verify_password(password, user.password):
            login_user(user)

            response['status'] = 'successs'
            response['message'] = 'user successfully logged in'
            code = 202
        else:
            response['status']: 'failure'
            response['message']: f'invalid email or password'
    except Exception as e:
        response['error'] = str(e)

    return jsonify(response), code


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    """Deletes the current user's session"""
    response = dict()

    try:
        logout_user()
        response['status'] = 'success'
        response['message'] = f'logged out user'
        code = 200
    except Exception as e:
        response['status'] = 'failure'
        response['message'] = f'could not log out user'
        response['error'] = str(e)
        code = 400

    return jsonify(response), code
