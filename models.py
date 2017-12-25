import time
import os
<<<<<<< HEAD
from bs4 import BeautifulSoup
=======
import sqlite3

>>>>>>> dev

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
			</body>
			""".format(self.title,self.title,self.content))
		self.file.close()

	def save(self,content):
		self.conn.execute("""INSERT INTO posts (title, author, datetime, timestamp,path) VALUES('{}','{}','{}','{}','{}')
			""".format(self.title,self.author,self.datetime,self.timestamp,
				os.path.join(self.post_directory,
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
