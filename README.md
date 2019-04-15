# Hobbs

Hobby Tracking App

Hobbs is a personal hobby trackering app that allows you to share or build your skills with a community that shares your interests.
With Hobbs you will be able to track events you're hosting and attending. Videos are available to help you get started or continue your develop. 
If there is a fellow enthusiast you would like to keep track, Hobbs allows you to follow other users.



---

## Technologies Used

appnope==0.1.0
backcall==0.1.0
bcrypt==3.1.6
certifi==2019.3.9
cffi==1.12.2
chardet==3.0.4
Click==7.0
decorator==4.3.2
dominate==2.3.5
Flask==1.0.2
Flask-Bcrypt==0.7.1
Flask-Bootstrap==3.3.7.1
Flask-Login==0.4.1
Flask-Rauth==0.3.2
Flask-WTF==0.14.2
idna==2.8
ipython==7.3.0
ipython-genutils==0.2.0
itsdangerous==1.1.0
jedi==0.13.3
Jinja2==2.10
MarkupSafe==1.1.1
parso==0.3.4
peewee==3.9.3
pexpect==4.6.0
pickleshare==0.7.5
prompt-toolkit==2.0.9
ptyprocess==0.6.0
pycparser==2.19
Pygments==2.3.1
rauth==0.7.3
requests==2.21.0
six==1.12.0
traitlets==4.3.2
urllib3==1.24.1
virtualenv==16.4.3
visitor==0.1.3
wcwidth==0.1.7
Werkzeug==0.15.1
WTForms==2.2.1


CSS Styling

Flask Bootstrap 

---

## Existing Features

Landing Page

- Authentication (User Log-In & Sign-Up)
  Sign-Up - On submission, will redirect to the login page
  Login - On submission, will redirec to user page

User Page

- Renders information based on Logged in User
  Displays
  Funcitionality

  - Username
  - User Image
  - User selected hobbies
  - Events User is hosting
    - Renders to the page based on events the user had created on the Main Page (Event Title, Location, Detail, Time)
    - Able to Read, Delete, and Update hosted events
  - Events User is Attending

    - Renders events the user has chosen to attend (Event Title, Location, Detail, Time)
    - Able to remove yourself from the event with an "Unattend" button
    
  - Other users the user is following or is being followed by. 
  
  Setting Page 
  
    - A user can click the "settings" button to edit their information. 
    - The button redirects the user to the settings page where the user can open
      a form to edit their details. 
    - The user is also able to add more hobbies on this page.
    - The user is also able to delete there account. 



Main Page

- Displays all the user's selected hobbies 
- A user can view videos per hobby for "starter videos" or "expert videos"
- User can create an event. 
- A user can click on the event logo to be taken to the events page. 


Single Event Page 

- User can edit/delete the event if they are the creator.
- A user can leave a comment on the event and edit or delete their own event. 

---

## Planned Future Features


- Have user see "default" profile photo on their profile page before adding their own photo
- Include Machine learning to recommend hobbies to a user.
- Send user a welcome email after creating an account
- Refract the site for better UI 
- Add Meetup API to replace user generated events on the app
- Add Strava and a few other APIs. 

---

##### Screenshot


<img src"https://github.com/Jonrosario5/Hobbs/blob/master/jon1.jpg.png" width="300px" />
<img src"../jon2.jpg.png" width="300px" />


---

#### Biggest Wins and Challenges

Wins

- Having users able to follow other users
- Having UI change based on whether the user is on a page where they created the content. 


Challenges

- Addning user followers
- UI 
- Heroku and Postgres migration 

---

