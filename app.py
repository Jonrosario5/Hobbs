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

meetup_blueprint = make_meetup_blueprint(key='f4d87i8qfkekdm33bj2lq43h',secret='7rm63mchjkl3cj1jtbb39m58iq')

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
    return render_template('index.html')

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
    events = models.Event.select()
    user_id = g.user._get_current_object().id
    event_form=forms.EventForm()
    user_hobbies = models.User_Hobby.select().where(
        models.User_Hobby.user_id == user_id )
    hobbies = models.Hobby.select()
    return render_template('main.html',hobbies=hobbies,user_hobbies=user_hobbies,event_form=event_form,events=events)




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
@app.route('/event/<eventid>',methods=['GET','POST'])
def events(eventid=None):
    form=forms.EventForm()
    if eventid != None:
        user_id = g.user._get_current_object().id
        events = models.Event.select().where(models.Event.id == eventid)
        attending = models.User_Event.select(models.User_Event.event_id).where(
        models.User_Event.user_id == user_id)

        comments = models.Comments.select().where(models.Comments.event_id == eventid)
        form = forms.Create_Event_Comments()
        edit_event_form = forms.EventForm()
        return render_template("single_event.html",events=events,form=form, comments=comments,edit_event_form=edit_event_form,attending=attending)

    else:    
        if form.validate_on_submit():
            models.Event.create_event(
                title=form.title.data,
                event_time=request.form.get('event_time'),
                location=form.location.data,
                details=form.details.data,
                hobby=form.hobby.data,
                created_by=g.user._get_current_object().id
                )

            event = models.Event.get(models.Event.title == form.title.data)

            models.User_Event.create_user_event(
                user=g.user._get_current_object(),
                event=event,
                isHost=True
            )
            
        return redirect(url_for('main')) 
    return render_template('event.html',form=form)

@app.route('/edit_event/<eventid>',methods=["GET","POST"])
def edit_events(eventid):

    form = forms.EventForm()
    if form.validate_on_submit():
        update_event = (models.Event.update(
            {models.Event.title: form.title.data,
             models.Event.location: form.location.data,
             models.Event.details: form.details.data,
             models.Event.event_time: request.form.get('event_time')
             })
            .where(models.Event.id == eventid))
        update_event.execute()


    return redirect(url_for('events', eventid=eventid))

@app.route('/delete_event/<eventid>')
def delete_event(eventid):
    print("get here")
    user = g.user._get_current_object()

    delete_user_event = models.User_Event.delete().where(models.User_Event.user_id == user.id and models.User_Event.event_id == eventid)
    delete_user_event.execute()
    delete_event_comments = models.Comments.delete().where(models.Comments.event_id == eventid and models.Comments.user_id == user.id)
    delete_this_event = models.Event.delete().where(models.Event.created_by_id == user.id and models.Event.id == eventid)
    delete_this_event.execute()


    return redirect(url_for('main'))

@app.route('/attend/<eventid>', methods=['GET', 'POST'])
def attend_event(eventid):
    user_events_count = models.User_Event.select().where((models.User_Event.user_id ==
                                                           g.user._get_current_object().id) & (models.User_Event.event_id == eventid)).count()

    if eventid != None and user_events_count <= 0:
        models.User_Event.create_user_event(
            user=g.user._get_current_object(),
            event=eventid,
            isHost=False
        )
    return redirect(url_for('events', eventid=eventid))

@app.route('/unattend/<eventid>', methods=['GET', 'POST'])
def unattend_event(eventid=None):
    user = g.user._get_current_object()
    if eventid != None:
        unattend_this_event = models.User_Event.delete().where(
            models.User_Event.user_id == user.id and models.User_Event.event_id == eventid)
        unattend_this_event.execute()

    return redirect(url_for('events',eventid=eventid))


@app.route('/profile',methods=['GET','POST'])
@app.route('/profile/<userid>',methods=['GET','POST'])
def user_profile(userid = None):
    
    if userid != None:
        user = models.User.select().where(models.User.id == userid)
        not_current_user_id = user.get()
        user_hobbies = models.User_Hobby.select().where(models.User_Hobby.user_id == userid)
        user_hobbies_count = user_hobbies.count()
        user_events = models.User_Event.select().where(models.User_Event.user == userid)
        user_events_count = user_events.count()
        current_follower_id = models.Follower.select().where(models.Follower.user == not_current_user_id and models.Follower.follower == g.user._get_current_object().id ).exists()
        isFollowing = False
        if current_follower_id != False:
            isFollowing = True
        user_followers = models.Follower.select().where(models.Follower.user == userid)
        user_followings = models.Follower.select().where(models.Follower.follower == userid)
        user_followers_count = models.Follower.select().where(models.Follower.user == userid).count()
        user_followings_count = models.Follower.select().where(models.Follower.follower == userid).count()

        return render_template('profile.html', user=user,user_hobbies=user_hobbies,user_hobbies_count=user_hobbies_count,user_events=user_events,user_events_count=user_events_count,user_followers=user_followers,user_followings=user_followings,not_current_user_id=not_current_user_id,user_followers_count=user_followers_count,user_followings_count=user_followings_count, isFollowing=isFollowing)
    else:
        user = g.user._get_current_object()
        user_id = g.user._get_current_object().id
        form = forms.Edit_UserForm()
        hours_spent_form = forms.Hours_SpentForm()
        hobbies = models.Hobby.select()
        user_hobbies = models.User_Hobby.select().where(models.User_Hobby.user == user_id)
        user_hobbies_count = user_hobbies.count()
        user_events = models.User_Event.select().where(models.User_Event.user == user_id)
        user_events_count = user_events.count()
        user_followers = models.Follower.select().where(models.Follower.user == user_id)
        user_followings = models.Follower.select().where(models.Follower.follower == user_id)
        user_followers_count = models.Follower.select().where(models.Follower.user == user_id).count()
        user_followings_count = models.Follower.select().where(models.Follower.follower == user_id).count()

        return render_template ('profile.html',form=form,user=user,hobbies=hobbies,user_hobbies=user_hobbies,hours_spent_form=hours_spent_form,user_hobbies_count=user_hobbies_count,user_events=user_events,user_events_count=user_events_count,user_followers=user_followers, user_followings=user_followings,user_followers_count=user_followers_count,user_followings_count=user_followings_count)

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

@app.route('/comments',methods=["GET","POST"])
@app.route('/comments/<commentsid>', methods=["GET","POST"])
def event_comments(commentsid=None):
    userid = g.user._get_current_object().id
    form = forms.Create_Event_Comments()

    if commentsid != None:
        if form.validate_on_submit:
            print("Comment Updated!")
            update_comments = models.Comments.update({models.Comments.body:form.body.data}).where(models.Comments.id == commentsid)
            update_comments.execute()

    else:
        if form.validate_on_submit:
        
            models.Comments.create_comment(
                user=userid,
                event=form.eventid.data,
                body=form.body.data)
            
    return redirect(url_for('events',eventid=form.eventid.data))

@app.route('/delete_comment/<commentsid>/<eventid>', methods=["GET","POST"])
def delete_comments(commentsid,eventid):

    delete_comment = models.Comments.delete().where(models.Comments.user_id == g.user._get_current_object().id and models.Comments.id == commentsid)
    delete_comment.execute()

    return redirect(url_for('events',eventid=eventid))





        
@app.route('/followers/<userid>',methods=["GET","POSTS"])
def user_followers(userid):
    print(userid)
    follower = g.user._get_current_object().id

    models.Follower.create_user_friend(
        user=userid,
        follower=follower
        )

    return redirect(url_for('user_profile',userid = userid))

@app.route('/unfollow/<userid>', methods=["GET","POST"])
def unfollow_user(userid):
    unfollow = models.Follower.delete().where(models.Follower.user_id == userid and
    models.Follower.follower_id == g.user._get_current_object().id)
    unfollow.execute()
    

    return redirect(url_for('user_profile',userid = userid))
 
                                            

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
