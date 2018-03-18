import time
import os
import sqlite3
import hashlib

class Blogpost:
	def __init__(self,id=None):
		self.conn = sqlite3.connect('data.db')
		self.id = id

		self.author = None
		self.title = None
		self.content = None
		self.datetime = None
		self.timestamp = None
				
	def save(self,title,author,content):
		self.conn.execute("""INSERT INTO posts (title, author, datetime, timestamp, content) VALUES('{}','{}','{}',
			'{}',"{}")
			""".format(title , author , time.ctime() , time.time() , content ))
		self.conn.commit()

	def set_data(self):
		cur = self.conn.execute("SELECT title FROM posts WHERE id = '{}' ".format(self.id))
		for x in cur:
			self.title =  x[0]
			break

		cur = self.conn.execute("SELECT author FROM posts WHERE id = '{}' ".format(self.id))
		for x in cur:
			self.author = x[0]
			break

		cur = self.conn.execute("SELECT content FROM posts WHERE id = '{}' ".format(self.id))
		for x in cur:
			self.content = x[0]
			break

		cur = self.conn.execute("SELECT datetime FROM posts WHERE id = '{}' ".format(self.id))
		for x in cur:
			self.datetime = x[0]
			break

		cur = self.conn.execute("SELECT timestamp FROM posts WHERE id = '{}' ".format(self.id))
		for x in cur:
			self.timestamp = x[0]
			break


class User:
	def __init__(self,username,name=None,email=None,password=None):
		self.conn = sqlite3.connect('data.db')
		self.username = username
		self.name = name
		self.email = email
		self.password = password
	
	def register(self,bio,avatar):
		if self.name == "" or self.email == "" or self.password == "":
			return 1

		if avatar == "":
			avatar = "/static/img/avatar.png"

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
			self.conn.execute("INSERT INTO users (name,username,email,password,bio,avatar) VALUES('{}','{}','{}','{}','{}','{}')"
.format(self.name,self.username,self.email,password_hashed.hexdigest(),bio,avatar))
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
	
	def get_bio(self):
		cur = self.conn.execute("SELECT bio FROM users WHERE username = '{}' ".format(self.username))
		for x in cur:
			return x[0]	
	def get_avatar(self):
		cur = self.conn.execute("SELECT avatar FROM users WHERE username = '{}' ".format(self.username))
		for x in cur:
			return x[0]
	
