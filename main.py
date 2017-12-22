from flask import Flask, render_template,request,url_for,make_response,redirect,session
import os
import time
from bs4 import BeautifulSoup
import sqlite3
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = "HelloWorld"

@app.route('/')
def index():
	try:
		loggedin = session['loggedin']
	except:
		session['loggedin'] = False
		loggedin = session['loggedin']
	
	post_directory = os.path.join('templates','blogposts')
	post_dirs = os.listdir(post_directory)

	post_content = []
	
	for folder in post_dirs:
		post_folder = os.path.join(post_directory,folder)
		posts = os.listdir(post_folder)

		for item in posts:
			post_text =	BeautifulSoup(open(os.path.join(post_folder,item),'r').read(),'html.parser')
			post_content.append(post_text)

			
	return render_template('home.html',loggedin=loggedin,post_content=post_content)

@app.route('/login',methods = ['GET','POST'])
def login():
	connection = sqlite3.connect('blog-data.db')

	if request.method == 'GET':
		return render_template('login.html',strike=0)	

	elif request.method == 'POST':

		username = request.form['username']
		password = request.form['password']

		result = connection.execute('SELECT * FROM users WHERE username="{}" AND password="{}"'
			.format(username,password))
		for user in result:
			session['loggedin'] = True
			session['username'] = username
			return redirect('/')
		return render_template('login.html',strike=1)
		

@app.route('/newpost',methods=['GET','POST'])
def newpost():
	loggedin = session['loggedin']
	post_author = session['username']

	if request.method == 'GET':
		return render_template('newpost.html',loggedin=loggedin)

	elif request.method == 'POST':
		if loggedin:			
			# do some stuff
			post_content = request.form['content']
			post_title = request.form['title']

			post_directory = ""
			try:
				os.mkdir(os.path.join(os.path.join('templates','blogposts'),post_author))
			except:
				pass
			
			post_directory = os.path.join(os.path.join('templates','blogposts'),post_author)
			file = open(os.path.join(post_directory,post_title),'w')

			file.write("""<title>{}</title>
				<body>
				<div class="container hero"><h1>{}</h1><hr></div><div class="container"><p>{}</p></div>
				</body>
				<div style="display: none;" id="metadata">
				<div id="time">{}</div>
				<div id="author">{}</div>
				""".format(post_title,post_title,post_content,time.ctime(),session['username']))
			file.close()

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
	loggedin = request.cookies.get('loggedin')

	post_directory = os.path.join(os.path.join(os.path.join('templates','blogposts'),post_author),'{}.html'
		.format(entry))
	post_content = open(post_directory,'r').read()
	
	return render_template('blogpost.html',title=entry, post_link=entry,loggedin=loggedin)

@app.route('/register',methods=['GET','POST'])
def register():
	connection = sqlite3.connect('blog-data.db')
	try:
		connection.execute('''CREATE table users(name varchar(60),
		 username varchar(40),email varchar(40),password varchar(40))''')
	except:
		pass

	if request.method == 'GET':
		return render_template('register.html',strike=0)
	
	else:
		#name = request.form['full-name']
		name = 'Ishaan'
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		password_confirm = request.form['password-confirm']

		cur = connection.execute('SELECT * FROM users WHERE username ="{}"'.format(username))
		for item in cur:
			return render_template('register.html',strike=1)
		cur = connection.execute('SELECT * FROM users WHERE email = "{}"'.format(email))
		
		for item in cur:
			return render_template('register.html',strike=2)
		
		if password != password_confirm:
			return render_template('register.html',strike=3)

		
		connection.execute('INSERT INTO  users VALUES("{}","{}","{}","{}")'
			.format(name,username,email,password))

		connection.commit()

		return str("registered")
		#return str(cur.execute('SELECT  * FROM  users'))

if __name__ == '__main__':
	app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 8080)),debug=True)