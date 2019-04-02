from flask_wtf import FlaskForm as Form

from models import Hobby
from models import User

from wtforms import StringField, PasswordField, TextAreaField, DateTimeField, BooleanField,SubmitField,HiddenField
from wtforms.widgets import ListWidget, CheckboxInput


from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,Length, EqualTo,Required)
from wtforms.fields.html5 import DateTimeField

def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')

class SignupForm(Form):
    username = StringField(
        'Username',validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                "numbers, and underscores only.")
            ),
            name_exists]
            )
    fullname = StringField(
        "Fullname",
        validators=[DataRequired()])

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists])

    bio = TextAreaField("Bio",validators=[DataRequired()])

    password = PasswordField(
        'Password',
        validators=[DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')])

    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()])
        


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class HobbyForm(Form):
    name = StringField('Name',validators=[DataRequired()])
    physical_activity = BooleanField('PA')
    outdoors = BooleanField('Outdoors')
    high_startup_cost = BooleanField('Entry_Costs')
    group_activity = BooleanField('GroupA')

class EventForm(Form):
    title = StringField('Title',validators=[DataRequired()])
    location = StringField('Location')
    details = TextAreaField('Details')
    hobby=StringField('Hobby')

class Edit_UserForm(Form):
    username = StringField("User")
    fullname = StringField("Fullname")
    bio = TextAreaField("Bio")
    

