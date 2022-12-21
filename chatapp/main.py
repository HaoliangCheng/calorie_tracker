from flask import Flask, request, redirect, render_template, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' 
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'} 
db=SQLAlchemy(app)

class User(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200),unique=True,nullable=False)
    passward = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),unique=True,nullable=False)

    def __init__(self,username,passward,email):
        self.username=username
        self.passward=passward
        self.email=email

class Chat(db.Model): 
    __bind_key__ = 'chat' 
    id =db.Column(db.Integer, primary_key=True)
    chatuser = db.Column(db.String(200),nullable=False)
    chatcontent = db.Column(db.String(200),nullable=False)
    datatime = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,chatuser,chatcontent):
        self.chatuser=chatuser
        self.chatcontent=chatcontent

    def serialize(self):
       return {
           'id' : self.id,
           'username' : self.chatuser,
           'message'  : self.chatcontent,
           'datatime' : self.datatime
       }


with app.app_context():
    db.create_all()
  
@app.route("/") 
def default(): 
    return redirect(url_for("login_controller"))
    
@app.route("/login/", methods=["GET", "POST"]) 
def login_controller(): 
    if(request.method=="GET"):
        return render_template("loginPage.html")
    else:
        user = User.query.filter_by(username=request.form['user_name']).first()

        if user and user.passward == request.form['user_password']:
            return redirect(url_for('profile',username=request.form['user_name']))
        else:
            return render_template("loginPage.html")

@app.route("/register/", methods=["GET", "POST"]) 
def register_controller(): 
    if(request.method=="GET"):
        return render_template("registerPage.html")
    else:
        user1 = User.query.filter_by(email=request.form['email']).first()
        user2 = User.query.filter_by(username=request.form['user']).first()

        if user1 or user2:
            return render_template("registerPage.html")
        elif request.form['Password']==request.form['RePassword']:
            Useranme =request.form['user']
            Email =request.form['email']
            Passward =request.form['Password']
            newUser= User(username=Useranme,email=Email,passward=Passward)
            try:
               db.session.add(newUser)
               db.session.commit()
               return redirect(url_for('profile', username=Useranme))
            except:
               return 'There was an issue adding your task'
        else:
            return render_template("registerPage.html")
            
@app.route("/profile/<username>") 
def profile(username=None): 
    if request.method == "POST":
        return render_template("chatPage.html", username=username)
    else:
        return render_template("chatPage.html", username=username)
 
@app.route("/logout/") 
def unlogger(): 
     return render_template("logoutPage.html")
    
@app.route("/new_message/", methods=["POST"]) 
def new_message(): 
    Username =request.form['username']
    message =request.form['message']
    newmessage= Chat(chatuser=Username,chatcontent=message)
    try:
        db.session.add(newmessage)
        db.session.commit()
    except:
        return 'There was an issue adding your task'
    
@app.route("/messages/") 
def messages(): 
    allmessages = Chat.query.order_by(Chat.datatime).all()
    list_serialized = [message.serialize() for message in allmessages]
    return jsonify(list_serialized)

    
if __name__=="__main__":
  app.run(threaded=True)
