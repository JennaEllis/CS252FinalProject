import json
from app import app, db
from app.views.auth import SignupForm, LoginForm
from app.models.user import User, Role

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security import current_user, login_user, login_required, logout_user
from flask_security.utils import hash_password, verify_password

auth = Blueprint('auth', __name__)


# Setup for Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@auth.route('/signup', methods=['GET', 'POST'])
def signup_page():
    """Displays the signup page"""
    form = SignupForm(request.form)

    if request.method == 'GET':
        return render_template('auth/signup.html', form=form)

    # validate the user's input
    if not form.validate():
        flash('error Invalid Input Provided. Please Try Again.')
        return redirect(url_for('auth.signup_page'))

    name = form['name'].data
    email = form['email'].data
    password = form['password'].data

    response = json.loads(signup(dict(
        name=name,
        email=email,
        password=password
    ))[0])

    if response['status'] == 'failure':
        flash('error {}'.format(response['message']))
        return redirect(url_for('auth.signup_page'))

    if response['status'] != 'success':
        flash('error An Error has Occured. Please Try Again.')
        return redirect(url_for('auth.signup_page'))

    flash('success Successfully Created Acount. Please Log In.')
    return redirect(url_for('auth.login_page'))


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    """Displays the login page"""
    form = LoginForm(request.form)

    if request.method == 'GET':
        return render_template('auth/login.html', form=form)

    # validate the user's input
    if not form.validate():
        flash('error Invalid Input Provided. Please Try Again.')
        return redirect(url_for('auth.signup_page'))

    email = form['email'].data
    password = form['password'].data

    response = json.loads(login(dict(
        email=email,
        password=password
    ))[0])

    if response['status'] == 'failure':
        flash('error {}'.format(response['message']))
        return redirect(url_for('auth.login_page'))

    if response['status'] != 'success':
        flash('error {} An Error has Occured. Please Try Again.'.format(response['status']))
        return redirect(url_for('auth.login_page'))

    flash('success Welcome, {}.'.format(current_user.name))
    return redirect('/')


@auth.route('/request/signup', methods=['POST'])
def signup(local_input=None):
    """Adds a new user to the database"""
    if local_input is None:
        data = request.get_json()
    else:
        data = local_input

    email = data['email']
    name = data['name']
    password = hash_password(data['password'])

    response = dict()

    try:
        db.session.add(User(email=email, name=name, password=password))
        db.session.commit()

        response['status'] = 'success'
        response['message'] = f'{email} was added'
        code = 201
    except Exception as e:
        response['status'] = 'failure'
        response['message'] = f'user already exists'
        response['error'] = str(e)
        code = 404

    response['code'] = code
    return json.dumps(response), code


@auth.route('/request/login', methods=['POST'])
def login(local_input=None):
    """Creates a session for the current user"""
    if local_input is None:
        data = request.get_json()
    else:
        data = local_input

    email = data['email']
    password = data['password']

    response = dict()

    try:
        user = User.query.filter_by(email=email).first()

        if verify_password(password, user.password):
            login_user(user)

            response['status'] = 'success'
            response['message'] = 'user successfully logged in'
            code = 202
        else:
            response['status']: 'failure'
            response['message']: 'invalid email or password'
    except Exception as e:
        response['error'] = str(e)
        code = 400

    response['code'] = code
    return json.dumps(response), code


@auth.route('/request/logout', methods=['GET'])
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

    return json.dumps(response), code
