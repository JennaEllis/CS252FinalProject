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
from app.controllers.create import create
from app.controllers.read import read
from app.controllers.delete import delete

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(create, url_prefix='/create')
app.register_blueprint(read, url_prefix='/read')
app.register_blueprint(delete, url_prefix='/delete')


@app.before_first_request
def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
