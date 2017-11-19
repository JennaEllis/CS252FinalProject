from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import InputRequired


class SignupForm(Form):
    name = StringField('name', validators=[InputRequired(), validators.Length(min=4, max=25)])
    email = StringField('email', validators=[InputRequired(), validators.Length(min=3, max=30)])
    password = PasswordField('password', validators=[InputRequired(), validators.Length(min=5, max=50)])
