#Forms stuff from Flask lecture to go in here
#Have to add secret_key somewhere? Not in text form in other py file because bad security
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', [Length(min=4, max=25)])
    email = StringField('Email Address', [Length(min=6, max=35)])
    firstname = StringField('Firstname', [Length(min=1, max=30)])
    lastname = StringField('Lastname', [Length(min=1, max=30)])
    password = PasswordField('New Password', [DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        u = User.query.filter_by(username=username.data).first()
        if u:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        u = User.query.filter_by(email=email.data).first()
        if u:
            raise ValidationError('Email already registered.')

#https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/ for forms tutorial