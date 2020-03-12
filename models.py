import os
import datetime
from peewee import *

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from playhouse.db_url import connect

#Adding Comments 


# DATABASE = SqliteDatabase('hobbs.db')
# DATABASE = PostgresqlDatabase('Hobbs')
DATABASE = connect(os.environ.get('DATABASE_URL'))



class Hobby(Model):
    name = CharField(50, unique= True)
    physical_activity = BooleanField()
    outdoors = BooleanField()
    high_startup_cost = BooleanField()
    group_activity = BooleanField()

    class Meta:
        database=DATABASE

    @classmethod
    def create_hobby(cls,name,physical_activity,outdoors,high_startup_cost,group_activity):
        cls.create(
            name = name,
            physical_activity = physical_activity,
            outdoors=outdoors,
            high_startup_cost =high_startup_cost,
            group_activity = group_activity
        )

class User(UserMixin, Model):
    username = CharField(unique=True)
    fullname = CharField()
    email = CharField(unique =True)
    password = CharField(max_length = 100)
    bio = TextField(300)
    dob = DateTimeField()
    isAdmin = BooleanField(default=False)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls,username,fullname,email,password,bio, dob,admin=False):
        try:
            cls.create(
                username=username,
                fullname=fullname,
                email=email,
                password=generate_password_hash(password),
                bio=bio,
                dob=dob,
                isAdmin= admin
            )
        except IndentationError:
            raise ValueError("User Already Exists")

class User_Hobby(Model):
    user=ForeignKeyField(model=User, backref="user")
    hobby=ForeignKeyField(model=Hobby, backref="hobby")
    hours_spent= BigIntegerField()

    class Meta:
        database=DATABASE
    
    @classmethod
    def create_user_hobby(cls,user,hobby,hours_spent=0):
        cls.create(
            user=user,
            hobby=hobby,
            hours_spent=hours_spent
        )
class Follower(Model):
    user=ForeignKeyField(model=User, backref="user")
    follower=ForeignKeyField(model=User,backref="follower")

    class Meta:
        database=DATABASE
    
    @classmethod
    def create_user_friend(cls,user,follower):
        cls.create(
            user=user,
            follower=follower
        )


class Event(Model):
    title=CharField()
    event_time=DateTimeField()
    location=CharField()
    details=TextField()
    hobby=ForeignKeyField(model=Hobby, backref="hobby") 
    created_by=ForeignKeyField(model=User, backref="user")

    class Meta:
        database=DATABASE
    
    @classmethod
    def create_event(cls,title,event_time,location,details,hobby,created_by):
        cls.create(
            title=title,
            event_time=event_time,
            location=location,
            details=details,
            hobby=hobby,
            created_by=created_by)
class Comments(Model):
    body=TextField(200)
    user=ForeignKeyField(model=User, backref="user")
    event=ForeignKeyField(model=Event, backref="event")

    class Meta:
        database=DATABASE

    @classmethod
    def create_comment(cls,user,event,body):
        cls.create(
            user=user,
            event=event,
            body=body)

class User_Event(Model):
    user=ForeignKeyField(model=User, backref="user")
    event=ForeignKeyField(model=Event, backref="event")
    isHost = BooleanField()

    class Meta:
        database=DATABASE
        
    @classmethod
    def create_user_event(cls,user,event,isHost=True):
        cls.create(
            user=user,
            event=event,
            isHost=isHost
        )

class User_Comments(Model):
    comment=ForeignKeyField(model=Comments, backref="comment")
    user=ForeignKeyField(model=User, backref="user")

    class Meta:
        database=DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Hobby,User,User_Hobby,Follower,Event,User_Event,Comments,User_Comments], safe=True)
    DATABASE.close()


