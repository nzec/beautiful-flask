import time
import os
from bs4 import BeautifulSoup

class Blogpost:
	def __init__(self,title,author):
		self.title = title
		self.author = author
		self.datetime = time.ctime()
		self.timestamp = time.time()
		self.post_directory = self.make_directory()
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

	def list(self,author=None):
		root = os.path.join('templates','blogposts')
		post_content = []
		
		if author == None:
			
			folders = os.listdir(root)
			for folder in folders:
				posts = os.listdir(os.path.join(root,folder))
				for post in posts:					
					post_text =	BeautifulSoup(open(os.path.join(os.path.join(root,folder),post),'r')
						.read(),'html.parser')
					post_content.append(post_text)
		else:
			folder = os.path.join(root,author)
			posts = os.listdir(folder)
			for post in posts:
				post_text =	BeautifulSoup(open(os.path.join(folder,post),'r')
						.read(),'html.parser')
				post_content.append(post_text)
		return post_content