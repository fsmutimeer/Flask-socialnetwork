from flask_wtf import FlaskForm
from wtforms import  StringField,PasswordField, IntegerField, SubmitField, TextField
from wtforms.validators import DataRequired,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from project.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password= PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired()])
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('confirm_password',message='Passwords Must match!')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])

    submit =SubmitField('Register')

    def check_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Your Email has already registered")
    def check_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('username has taken!')

class UpdateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','mp4'])])

    submit = SubmitField('Update Profile')


    def check_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Your Email has already registered")
    def check_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('username has taken!')
