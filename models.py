import datetime
from peewee import *

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('hobbs.db')

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

    class Meta:
        database=DATABASE
    
    @classmethod
    def create_user_hobby(cls,user,hobby):
        cls.create(
            user=user,
            hobby=hobby
        )
class User_Friend(Model):
    user=ForeignKeyField(model=User, backref="user")
    user_friend=ForeignKeyField(model=User,backref="user_friend")

    class Meta:
        database=DATABASE
    
    @classmethod
    def create_user_friend(cls,user,user_friend):
        cls.create(
            user=user,
            user_friend=user_friend
        )


class Event(Model):
    title=CharField()
    event_time=DateTimeField()
    location=CharField()
    details=TextField()
    hobby=ForeignKeyField(model=Hobby, backref="hobby") 

    class Meta:
        database=DATABASE
    
    @classmethod
    def create_event(cls,title,event_time,location,details,hobby):
        cls.create(
            title=title,
            event_time=event_time,
            location=location,
            details=details,
            hobby=hobby)


class User_Event(Model):
    user=ForeignKeyField(model=User, backref="user")
    event=ForeignKeyField(model=Event, backref="event")

    class Meta:
        database=DATABASE
        
    @classmethod
    def create_user_event(cls,user,event):
        cls.create(
            user=user,
            event=event
        )

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Hobby,User,User_Hobby,User_Friend,Event,User_Event], safe=True)
    DATABASE.close()


