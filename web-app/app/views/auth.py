from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class SignupForm(FlaskForm):
    name = StringField('name',
        validators=[DataRequired(), validators.Length(min=4, max=25)])
    email = StringField('email',
        validators=[DataRequired(), validators.Length(min=3, max=30)])
    password = PasswordField('password',
        validators=[DataRequired(), validators.Length(min=5, max=50)])
