from flask import Flask, render_template,request,url_for,make_response,redirect
import os
import datetime
from bs4 import BeautifulSoup
import sqlite3

app = Flask(__name__)
#cur.execute('CREATE table users(name varchar(60), username varchar(40),email varchar(40),password varchar(40))')

@app.route('/')
def index():
	loggedin = request.cookies.get('loggedin')
	post_directory = os.path.join(os.path.join('templates','blogposts'),'admin')

	post_content = []
	posts = os.listdir(post_directory)
	for item in posts:
		post_text =	BeautifulSoup(open(os.path.join(post_directory,item),'r').read()[:750],'html.parser')
		post_content.append(post_text)

	return render_template('home.html',loggedin=loggedin,post_content=post_content)

@app.route('/login',methods = ['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html',strike=0)	

	elif request.method == 'POST':

		username = request.form['username']
		password = request.form['password']

		resp = make_response(redirect('/'))

		if username == "admin" and password == "password":
			resp.set_cookie('loggedin',"True")
			return resp
		else:
			resp.set_cookie('loggedin',"False")
			return render_template('login.html',strike=1)

@app.route('/newpost',methods=['GET','POST'])
def newpost():
	loggedin = request.cookies.get('loggedin')

	if request.method == 'GET':
		return render_template('newpost.html',loggedin=loggedin)

	elif request.method == 'POST':
		if loggedin == "True":			
			# do some stuff
			post_content = request.form['content']
			post_title = request.form['title']

			post_directory = os.path.join(os.path.join('templates','blogposts'),'admin')
			file = open(os.path.join(post_directory,'{}.html'.format(post_title)),'w')

			file.write("""<title>{}</title>
				<body>
				<div class="container hero"><h1>{}</h1><hr></div><div class="container"><p>{}</p></div>
				</body>""".format(post_title,post_title,post_content))
			file.close()

			return render_template('success.html',link=post_title)
		else:
			return "Please log in to continue!"

@app.route('/logout')
def logout():
	resp = make_response(redirect('/'))
	resp.set_cookie('loggedin','False')
	return resp

@app.route('/<entry>/')
def viewpost(entry):
	loggedin = request.cookies.get('loggedin')
	post_directory = os.path.join(os.path.join(os.path.join('templates','blogposts'),'admin'),'{}.html'.format(entry))
	post_content = open(post_directory,'r').read()
	
	return render_template('blogpost.html',title=entry, post_link=entry,loggedin=loggedin)

@app.route('/register',methods=['GET','POST'])
def register():
	connection = sqlite3.connect('blog-data.db')

	cur = connection.cursor()

	if request.method == 'GET':
		return render_template('register.html')
	
	else:
		name = request.form['name']
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cur.execute('insert into users values("{}","{}","{}","{}")'.format(name,username,email,password))
		connection.commit()
		connection.close()
	
		connection = sqlite3.connect('blog-data.db')
		cur = connection.cursor()


		return str(cur.execute('select * from users'))

if __name__ == '__main__':
	app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)
	#app.run(port=8080,debug=True,host="0.0.0.0")
