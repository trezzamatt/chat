from tokenize import String
from xml.dom.minidom import Document
from flask import Flask, redirect, render_template, request, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dataclasses import dataclass

from sqlalchemy import null

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'}
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@dataclass
class Chat(db.Model):
    id: int
    author: str
    message: str

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(280), nullable=False)

    __bind_key__ = 'chat'
    def __repr__(self):
        return '<Chat %r>' % self.id

@app.route("/")
def default():
    return redirect(url_for('login_controller'))

@app.route("/login/", methods=["GET", "POST"])
def login_controller():
    if (request.method == 'POST'):
        db_entry=User.query.filter_by(username=request.form["username"], password=request.form["password"]).first()
        if db_entry is None:
            return render_template('loginPage.html')
        else:
            session['user'] = request.form['username']
            return redirect(url_for('profile', username=request.form["username"]))
    else:
        return render_template('loginPage.html')
 
@app.route("/register/", methods=["GET", "POST"])
def register_controller():
    if (request.method == 'POST'):
        if (request.form["password"] == request.form["retype"]):
            db.session.add(User(username=request.form["username"], email=request.form["email"], password=request.form["password"]))
            db.session.commit()
            session['user'] = request.form['username']
            return redirect(url_for('profile', username=request.form["username"]))
        else:
            return render_template('register.html')
    else:
        print("passwords do not match")
        return render_template('register.html')
 
@app.route("/profile/<username>")
def profile(username):
    return render_template('chat_page.html', username=username)

@app.route("/logout/")
def unlogger():
    session['user'] = None
    return redirect(url_for('login_controller'))

@app.route("/new_message/", methods=["POST"])
def new_message():
    db.session.add(Chat(author=session['user'], message=request.form['message']))
    db.session.commit()
    return Chat.query.all()
    

@app.route("/messages/")
def messages():
    return Chat.query.all()

if __name__ == "__main__":
	app.run()
