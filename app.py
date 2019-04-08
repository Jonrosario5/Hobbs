import os
from flask import Flask, g
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from flask_dance.contrib.meetup import make_meetup_blueprint, meetup
from flask_bootstrap import Bootstrap

from peewee import *

import models
import forms
import json
from datetime import datetime

DEBUG = True
PORT = 7000

app = Flask(__name__)
app.secret_key = 'jonnyBuckets.yum'
Bootstrap(app)

meetup_blueprint = make_meetup_blueprint(key='gvl55f70d307mjj4r33cjgf4mh',secret='u3tsdfb671cob42alba31cdn45')

app.register_blueprint(meetup_blueprint, url_prefix='/meetup_login')



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


@app.route('/meetup')
def meetup_login():
    if not meetup.authorized:
        print('Working?')
        return redirect(url_for('meetup.login'))

    return '<h1>Request Failed<h1>'

@app.route('/')
def home():
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
        return redirect(url_for('login'))
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

                return redirect(url_for('user_profile'))
            else:
                flash("your email or password doesn't match", "error")
    return render_template('login.html', form=form)


@app.route('/logout',methods=['POST','GET'])
def logout():
    logout_user()
    flash("You've been logged out", 'success')
    return redirect(url_for('login'))

@app.route('/main',methods=['POST','GET'])
def main():
    user_id = g.user._get_current_object().id
    user_hobbies = models.User_Hobby.select().where(
        models.User_Hobby.user_id == user_id )
    hobbies = models.Hobby.select()
    return render_template('main.html',hobbies=hobbies,user_hobbies=user_hobbies)




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
        return redirect(url_for('home')) 
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
            
        return redirect(url_for('home')) 
    return render_template('event.html',form=form)

@app.route('/profile',methods=['GET','POST'])
def user_profile():
    user = g.user._get_current_object()
    user_id = g.user._get_current_object().id
    form = forms.Edit_UserForm()
    hours_spent_form = forms.Hours_SpentForm()
    hobbies = models.Hobby.select()
    user_hobbies = models.User_Hobby.select().where(models.User_Hobby.user == user_id)
    user_hobbies_count = user_hobbies.count()
    user_events = models.User_Event.select().where(models.User_Event.user == user_id)
    user_events_count = user_events.count()


    return render_template ('profile.html',form=form,user=user,hobbies=hobbies,user_hobbies=user_hobbies,hours_spent_form=hours_spent_form,user_hobbies_count=user_hobbies_count,user_events_count=user_events_count)

@app.route('/settings',methods=["GET","POST"])
def settings():
    form = forms.Edit_UserForm()
    user = g.user._get_current_object()
    hobbies = models.Hobby.select()

    return render_template('edituser.html',form=form,user=user,hobbies=hobbies)


@app.route('/userupdate',methods=['GET','POST'])
def edit_user():
    form = forms.Edit_UserForm()
    user_id = g.user._get_current_object().id
    hobbies = models.Hobby.select()
    print(user_id)
    print(form.bio.data)

    if form.validate_on_submit:
        update_user = (models.User.update(
            {models.User.fullname: form.fullname.data,
            models.User.username: form.username.data,
            models.User.bio: form.bio.data})
            .where(models.User.id == user_id))
        print(update_user)

        update_user.execute()

        return redirect(url_for('user_profile'))
    
@app.route('/deleteuser',methods=["GET", "POST"])
def delete_user():
    user_id = g.user._get_current_object().id
    delete_user_button = models.User.delete().where(models.User.id == user_id)
    delete_user_button.execute()

    return redirect('signup')

@app.route('/userhobbies/<hobbyid>',methods=["GET","POST"])
def add_user_hobbies(hobbyid=None):
    user_id = g.user._get_current_object().id


    if hobbyid != None:
        user_hobbies_count = models.User_Hobby.select().where((models.User_Hobby.user_id == user_id)
                                                              & (models.User_Hobby.hobby_id == hobbyid)).count()
        if user_hobbies_count > 0:
            flash('Already Exists')
            print('Working')
            return redirect(url_for('user_profile'))

        else:
            models.User_Hobby.create_user_hobby(
                user=user_id,
                hobby=hobbyid
            )
            return redirect(url_for('user_profile'))

    return redirect(url_for('user_profile'))

@app.route('/remove_user_hobbies/<user_hobbyid>',methods=["GET","POST"])
def delete_user_hobbies(user_hobbyid=None):
    userid = g.user._get_current_object().id
    
    if user_hobbyid != None:
        delete_user_hobby = models.User_Hobby.delete().where(models.User_Hobby.user == userid and models.User_Hobby.id == user_hobbyid)
        delete_user_hobby.execute()
        
        return redirect(url_for('user_profile'))

@app.route('/hours_spent/<user_hobbyid>',methods=["GET","POST"])
def hours_spent_increment(user_hobbyid=None):
    userid = g.user._get_current_object().id
    form = forms.Hours_SpentForm()

    if user_hobbyid != None:
        print("jello")
        if form.validate_on_submit:
            print('hello')
            increment_hobby_hours = models.User_Hobby.update(
               {models.User_Hobby.hours_spent:form.hours_spent}).where(
                   models.User_Hobby.id == user_hobbyid)
            increment_hobby_hours.execute()


    return redirect(url_for('user_profile'))
                                            

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
