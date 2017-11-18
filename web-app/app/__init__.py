from settings import init_env
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify

# create the app
init_env()
app = Flask(__name__)

# set config
app.config.from_object('app.config.DevelopmentConfig')

# set database
db = SQLAlchemy(app)


# import and register blueprints
from app.controllers.auth import auth

app.register_blueprint(auth, url_prefix='/auth')


@app.before_first_request
def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'success'})
