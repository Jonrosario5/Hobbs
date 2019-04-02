from flask import Flask, g
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from peewee import *

import models
import forms
import json
from datetime import datetime

DEBUG = True
PORT = 7000

app = Flask(__name__)
app.secret_key = 'jonnyBuckets.yum'

login_manager = LoginManager()
# sets up our login for the app
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response



@app.route('/')
def testing():
    return('Hi Jon')

@app.route('/signup', methods=["POST","GET"])
def register():
    form = forms.SignupForm()
    if form.validate_on_submit():
        flash("Successful signup!", 'success')
        models.User.create_user(
            username=form.username.data,
            fullname=form.fullname.data,
            email=form.email.data,
            bio=form.bio.data,
            dob=request.form.get('dob'),
            password=form.password.data
        )
        return redirect(url_for('testing'))
    return render_template('signup.html', form=form)

@app.route('/login',methods=['POST','GET'])
def login():
    form=forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email doesn't exist")
        else:
            if check_password_hash(user.password, form.password.data):
                # creates session
                login_user(user)
                flash("You've been logged in", "success")
                user_id = user.id

                return redirect(url_for('testing'))
            else:
                flash("your email or password doesn't match", "error")
    return render_template('login.html', form=form)

@app.route('/logout',methods=['POST','GET'])
def logout():
    logout_user()
    flash("You've been logged out", 'success')
    return redirect(url_for('testing'))




@app.route('/hobby',methods=['GET','POST'])
def hobbies():
    form =forms.HobbyForm()
    if form.validate_on_submit():
        models.Hobby.create_hobby(
            name=form.name.data,
            physical_activity = form.physical_activity.data,
            outdoors = form.outdoors.data,
            high_startup_cost = form.high_startup_cost.data,
            group_activity = form.group_activity.data
            )
        return redirect(url_for('testing')) 
    return render_template('hobby.html', form=form)


@app.route('/event',methods=['GET','POST'])
def events():
    form=forms.EventForm()
    # Change to API data from Meetup
    if form.validate_on_submit():
        models.Event.create_event(
            title=form.title.data,
            event_time=request.form.get('event_time'),
            location=form.location.data,
            details=form.details.data)
            
        return redirect(url_for('testing')) 
    return render_template('event.html',form=form)

@app.route('/profile',methods=['GET','POST'])
@app.route('/profile/<userid>')
def user_profile():
    user = g.user._get_current_object()
    form = forms.Edit_UserForm

    render_template ('profile.html',form=form,user=user)


 


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
