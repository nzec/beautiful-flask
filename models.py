import time
import os
import sqlite3
import hashlib

class Blogpost:

	def __init__(self,title=None,author=None):
		self.conn = sqlite3.connect('blog-data.db')
		self.title = title
		self.author = author
		self.datetime = time.ctime()
		self.timestamp = time.time()

		if self.author != None:
			self.post_directory = self.make_directory()
			self.post_id = self.remove_spaces()

	def write_to_file(self,content):
		self.content = content		
		self.file = open(os.path.join(self.post_directory,self.post_id+".html"),'w')
		self.file.write("""
			<title>{}</title>
			<body>
				<div class="container hero"><h1>{}</h1><hr></div><div class="container"><p>{}</p></div>
				</div>
			</body>
			<div id="metadata" style = "display: none">
			<div id = "author">{}</div>
			<div id = "datetime">{}</div>
			<div id = "post_id">{}</div>
			</div>
			""".format(self.title,self.title,self.content,self.author,self.datetime,self.post_id))
		self.file.close()

	def save(self,content):
		self.conn.execute("""INSERT INTO posts (title, author, datetime, timestamp,path) VALUES('{}','{}','{}',
			'{}','{}')
			""".format(self.title,self.author,self.datetime,self.timestamp,	os.path.join(self.post_directory,
				self.post_id+".html")))

		self.write_to_file(content)
		self.conn.commit()

	def remove_spaces(self):
		x=""
		for char in range(len(self.title)):
			if self.title[char] == " ":
				x+=""
			else:
				x+=self.title[char]
		return x
	
	def make_directory(self):
		try:
			os.mkdir(os.path.join(os.path.join('templates','blogposts'),self.author))
		except:
			pass
		return os.path.join(os.path.join('templates','blogposts'),self.author)

class User:
	def __init__(self,username,name=None,email=None,password=None):
		self.conn = sqlite3.connect('blog-data.db')
		self.username = username
		self.name = name
		self.email = email
		self.password = password
	
	def register(self):
		if self.name == "" or self.email == "" or self.password == "":
			return 1

		password_hashed = hashlib.new('sha224')
		password_hashed.update(bytes(self.password,'utf-8'))

		same_email_wale = self.conn.execute("SELECT * FROM users where email = '{}'".format(self.email))
		same_username_wale = self.conn.execute("SELECT * FROM users where username = '{}'".format(self.username))
		
		for x in same_username_wale:			
			return 2
			break
		for x in same_username_wale:			
			return 3
			break			
		else:
			self.conn.execute("INSERT INTO users (name,username,email,password) VALUES('{}','{}','{}','{}')"
				.format(self.name,self.username,self.email,password_hashed.hexdigest()))
			self.conn.commit()
			return 0

	
	def authenticate(self,uname,passwrd):
		cur = self.conn.execute("SELECT password FROM users where username='{}'".format(uname))

		for x in cur:			
			if hashlib.sha224(bytes(passwrd,'utf-8')).hexdigest() == x[0]:
				return True
				break

			else:
				return False
				break
		
	def user_homepage(self):
		cur = self.conn.execute("SELECT path FROM posts WHERE author = '{}' ORDER BY timestamp DESC"
			.format(self.username))
		return cur

	def get_name(self):
		cur = self.conn.execute("SELECT name FROM users WHERE username = '{}'".format(self.username))
		for x in cur:
			return x[0]

	def update_settings(self,name,bio):
		self.conn.execute("""UPDATE users SET name = {}, bio={} WHERE username={}""".format(name,bio,self.username))

	def exists(self):
		cur = self.conn.execute("SELECT * FROM users WHERE username='{}'".format(self.username))
		
		for x in cur:
			if x[0] is True:
				return False

			else:
				return True
			break
		