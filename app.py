#!/usr/bin/env python

from __future__ import print_function
from flask import Flask, render_template, redirect, url_for, \
  request, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
#import sqlite3

import sys
import optparse

app = Flask(__name__)

app.secret_key = 'yabadadbadoo'
app.database = "posts.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

# create SQLAlchemy object
db = SQLAlchemy(app)

from models import * 

def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)

def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
        return f(*args, **kwargs)
    else:
      flash('You need to login first.')
      return redirect(url_for('login'))
  return wrap

@app.route('/')
@login_required
def home():
  posts = db.session.query(BlogPost).all()
  return render_template('index.html', posts=posts)

@app.route('/welcome')
def welcome():
  return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != 'admin' or request.form['password'] != 'admin':
      error = 'Invalid Credentials. Please try again.'
    else:
      session['logged_in'] = True
      flash('You were just logged in')
      return redirect(url_for('home'))
  return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
  session.pop('logged_in', None)
  flash('You were just logged out!')
  return redirect(url_for('welcome'))

# def connect_db():
#   return sqlite3.connect(app.database)

if __name__ == '__main__':
  #parser = optparse.OptionParser(usage="flask-tut.py -p ")
    #parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
    #(args, _) = parser.parse_args()
    #if args.port == None:
    #    print "Missing required argument: -p/--port"
    #    sys.exit(1)


  app.run(host='0.0.0.0', port=5000, debug=True)
