from flask import Flask, render_template,request,url_for
import os
import datetime
import html2text
#from flaskext.mysql import MySQL

app = Flask(__name__)

# initializes mysql app
#mysql = MySQL()
#app.config['MYSQL_DATABASE_USER'] = 'ENTER YOUR USERNAME'
#  change the password
#app.config['MYSQL_DATABASE_PASSWORD'] = 'ENTER YOUR PASSWORD'
#app.config['MYSQL_DATABASE_DB'] = 'testing'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#mysql.init_app(app)

#cursor = mysql.connect().cursor()

@app.route('/')
def index():
	post_directory = os.path.join(os.path.join('templates','blogposts'),'admin')

	post_text = []
	post_links = []
	post_content = []
	posts = os.listdir(post_directory)
	for item in posts:
		post_content.append(html2text.html2text(open(os.path.join(post_directory,item),'r').read())[:300])
		#post_text.append(post_content.read())
		item = item[:-5]
		post_links.append(item)

	return render_template('home.html',posts=post_links,loggedin=True,post_content=post_content)

@app.route('/login',methods = ['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')	

	elif request.method == 'POST':

		username = request.form['username']
		password = request.form['password']

		cursor.execute("SELECT * from users where username ='" + username + "' and password='" + password + "'")
		data = cursor.fetchone()
		if data is None:
			return "Username or Password is wrong"
		else:
			return "Logged in successfully"

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html',user=user)

@app.route('/newpost',methods=['GET','POST'])
def newpost():
	if request.method == 'GET':
		return render_template('newpost.html')

	elif request.method == 'POST':
		# do some stuff
		post_content = request.form['content']
		post_title = request.form['title']

		post_directory = os.path.join(os.path.join('templates','blogposts'),'admin')
		file = open(os.path.join(post_directory,'{}.html'.format(post_title)),'w')

		file.write("""<div class="container hero"><h1>{}</h1><hr></div><div class="container"><p>{}</p></div>""".format(post_title,post_content))
		file.close()

		return render_template('success.html',link=post_title)

@app.route('/register',methods=['GET','POST'])
def register():
	if request.method == 'GET':
		return render_template('login.html')

	elif request.method =='POST':
		username = request.form['username']
		password = request.form['password']
		cursor.execute("insert into users values('{}','{}');".format(username,password))
		return "Registered"

@app.route('/<entry>/')
def viewpost(entry):
	post_directory = os.path.join(os.path.join(os.path.join('templates','blogposts'),'admin'),'{}.html'.format(entry))
	post_content = open(post_directory,'r').read()
	
	return render_template('blogpost.html',title=entry, post_link=entry)

if __name__ == '__main__':
	app.run(host=os.getenv('IP', 'localhost'),port=int(os.getenv('PORT', 8080)),debug=True)
	#app.run(port=8080,debug=True,host="0.0.0.0")
