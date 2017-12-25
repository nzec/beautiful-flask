from flask import Flask, render_template,request,url_for,make_response,redirect,session
from bs4 import BeautifulSoup
import sqlite3
import random
import models
import os
import socket


app = Flask(__name__)
app.config['SECRET_KEY'] = "HelloWorld"

def check_session():
	try:
		loggedin = session['loggedin']
	except:
		session['loggedin'] = False
		loggedin = session['loggedin']
	return loggedin

@app.route('/')
def index():
	loggedin = check_session()

	blogpost = models.Blogpost()

	posts = blogpost.conn.execute("SELECT path FROM posts ORDER BY timestamp DESC")

	post_content = []
	
	for post in posts:
		post_text =	BeautifulSoup(open(post[0],'r').read(),'html.parser')
		post_content.append(post_text)

	return render_template('home.html',loggedin=loggedin,post_content=post_content)

@app.route('/login',methods = ['GET','POST'])
def login():
	
	if request.method == 'GET':
		return render_template('login.html',strike=0)	

	elif request.method == 'POST':

		username = request.form['username']
		password = request.form['password']
		user = models.User(session['username'])
		
		result = user.authenticate(username,password)
		if result == False:
			session['loggedin'] = True
			session['username'] = username
			return redirect('/')
		return render_template('login.html',strike=1)
		

@app.route('/newpost',methods=['GET','POST'])
def newpost():
	loggedin = check_session()	

	if request.method == 'GET':
		return render_template('newpost.html',loggedin=loggedin)

	elif request.method == 'POST':
		
		if loggedin:			
			post_content = request.form['content']
			post_title = request.form['title']
			post_author = session['username']

			blogpost = models.Blogpost(post_title,post_author)
			blogpost.save(post_content)

			return render_template('success.html',link=post_title)
		else:
			return "Please log in to continue!"

@app.route('/logout')
def logout():
	session['loggedin'] = False
	session['username'] = None
	return redirect('/')

@app.route('/<post_author>/<entry>/')
def viewpost(entry,post_author):
	loggedin = check_session()

	post_directory = os.path.join(os.path.join(os.path.join('templates','blogposts'),post_author),'{}.html'
		.format(entry))
	post_content = open(post_directory,'r').read()
	
	return render_template('blogpost.html',title=entry, post_link=entry,loggedin=loggedin)

@app.route('/register',methods=['GET','POST'])
def register():
	
	
	if request.method == 'GET':
		return render_template('register.html',strike=0)
	
	else:

		name = request.form['full-name']
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		password_confirm = request.form['password-confirm']
		
		if password != password_confirm:
			return render_template('register.html',strike=4)
		
		user = models.User(username,name,email,password)
		strike = user.register()
		if strike != 0:
			return render_template('register.html',strike=strike)
		
		session['loggedin'] =True
		session['username'] = username
		
		return render_template('home.html',strike=2)

if socket.gethostname() == "DESKTOP-D18" :
	if __name__ == '__main__':
		app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 8080)),debug=True)
else :
	if __name__ == '__main__':
		app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)