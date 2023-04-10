from flask import Flask, request, redirect, render_template, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

from sqlalchemy import or_


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' 
db=SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'
    id =db.Column(db.Integer, primary_key=True, unique = True, nullable = False)
    username = db.Column(db.String(200),unique=True,nullable=False)
    passward = db.Column(db.String(200),nullable=False)
    age = db.Column(db.Integer,nullable=False)
    height = db.Column(db.Integer,nullable=False)
    weight = db.Column(db.Integer,nullable=False)
    goal_weight = db.Column(db.Integer,nullable=False)
    gender = db.Column(db.String(200),nullable=False)
    daily_caloire_goal = db.Column(db.Integer,nullable=False)
    date_of_creation = db.Column(db.String(200), default = datetime.utcnow().strftime('%Y-%m-%d'), nullable = False)

    def __init__(self,username,passward,age,height,weight,goal_weight,gender,daily_caloire_goal):
        self.username=username
        self.passward=passward
        self.age=age
        self.height=height
        self.weight=weight
        self.goal_weight=goal_weight
        self.gender=gender
        self.daily_caloire_goal=daily_caloire_goal

    def __repr__(self): #for debugging
        return '<Name %r>' % self.username
class diary(db.Model): 
#    __bind_key__ = 'diary' 
    id =db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200),nullable=False)
    calorie = db.Column(db.String(200),nullable=False)
    date = db.Column(db.String(200),nullable=False)

    def __init__(self,user,calorie,date):
        self.user=user
        self.calorie=calorie
        self.date=date

    def serialize(self):
       return {
           'id' : self.id,
           'username' : self.user,
           'calorie'  : self.calorie,
           'date': self.date
       }

class Food(db.Model):
    __tablename__ = 'Food'
    id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    name = db.Column(db.String(200), nullable = False)
    calories = db.Column(db.Integer, nullable = False)
    userID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable = False)

    def __repr__(self):
        return '<Name %r>' % self.name

class Exercise(db.Model):
    __tablename__ = 'Exercise'
    id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    name = db.Column(db.String(200), nullable = False)
    calories = db.Column(db.Integer, nullable = False)
    userID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable = False)

    def __repr__(self):
        return '<Name %r>' % self.name


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
        user1 = User.query.filter_by(username=request.form['user']).first()

        if user1:
            return render_template("registerPage.html")
        elif request.form['Password']==request.form['RePassword']:
            Useranme =request.form['user']
            age=request.form['age']
            gender=request.form['gender']
            height=request.form['height']
            weight=request.form['weight']
            goal_weight=request.form['goal_weight']
            daily_caloire_goal=request.form['daily_caloire_goal']
            Passward =request.form['Password']
            newUser= User(username=Useranme,
                          age=age,height=height,
                          weight=weight,
                          goal_weight=goal_weight,
                          gender=gender,
                          daily_caloire_goal=daily_caloire_goal,
                          passward=Passward)
            try:
               db.session.add(newUser)
               db.session.commit()
               return redirect(url_for('profile', username=Useranme))
            except:
               return 'There was an issue adding your task'
        else:
            return render_template("registerPage.html")
            
@app.route("/<username>/profile") 
def profile(username=None): 
    if request.method == "POST":
        return render_template("caloriePage.html", username=username)
    else:
        return render_template("caloriePage.html", username=username)
 
@app.route("/logout/") 
def unlogger(): 
     return render_template("logoutPage.html")

@app.route("/<username>/add_record/", methods=["GET", "POST"])
def add_record(username=None):
    user = User.query.filter_by(username=username).first()
    food_list = db.session.execute(db.select([Food.name]).where(or_(Food.userID == user.id, Food.userID == 0))).scalars().all()
    if request.method == "GET":
        return render_template("add_record.html", username=username, food_list=food_list)
    else:
        flag = 0
        date = request.form['date']
        food_l_ent = request.form['food_list']
        food = request.form['food']
        calorie0 = request.form['calories']
        amount = request.form['amount']

        if food == "":
            flag = 1
            food = food_l_ent
            calorie0 = db.session.execute(db.select([Food.calories]).where(Food.name == food)).scalars().first()

        calorie1 = str(int(calorie0) * int(amount))

        if flag == 0:
            diary_entry = diary(user=username, calorie=calorie1, date=date)
            food_entry = Food(name=food, calories=calorie0, userID=user.id)
        else:
            diary_entry = diary(user=username, calorie=calorie1, date=date)
        try:
            if flag == 0:
                db.session.add(food_entry)
            db.session.add(diary_entry)
            db.session.commit()
            return redirect(url_for('profile', username=username))
        except:
            return 'There was an issue adding your task'
    
if __name__=="__main__":
  app.run(threaded=True)
