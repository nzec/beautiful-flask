import time
import os
import sqlite3


class Blogpost:

	def __init__(self,title=None,author=None):
		self.conn = sqlite3.connect('blog-data.db')
		self.title = title
		self.author = author
		self.datetime = time.ctime()
		self.timestamp = time.time()
		#self.post_directory = self.make_directory()
		#self.post_id = self.remove_spaces()

	def write_to_file(self,content):
		self.content = content		
		self.file = open(os.path.join(self.post_directory,self.title),'w')
		self.file.write("""
			<title>{}</title>
			<body>
				<div class="container hero"><h1>{}</h1><hr></div><div class="container"><p>{}</p></div>
			</body>
			""".format(self.title,self.title,self.content))
		self.file.close()

	def save(self,content):
		self.conn.execute("""INSERT INTO posts VALUES('{}','{}','{}','{}','{}')
			""".format(self.title,self.author,self.datetime,self.timestamp,self.post_directory))

		self.write_to_file(content)
		self.conn.commit()

	def remove_spaces(self):
		for char in range(len(self.title)):
			print(char)
			if self.title[char] == " ":
				self.title[char] = ""
		return self.title
	
	def make_directory(self):
		try:
			os.mkdir(os.path.join(os.path.join('templates','blogposts'),self.author))
		except:
			pass
		return os.path.join(os.path.join('templates','blogposts'),self.author)
	
