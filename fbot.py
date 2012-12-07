#!/usr/bin/python
import facebook
import time
import string
import re
from threading import Timer
class fbotPost:
	"""Represents a post in a page"""
		
	def __init__(self, grph, pg, msg, postID=""):
		self.refreshRate=10.0
		self.stop=False
		self.listeners=[]
		self.graph=grph
		self.offset=0
		self.page=pg
		if (postID==""):
			print msg
			post=grph.put_object(pg, "feed", message=msg.encode('utf-8'))
			print("new post id: ",post["id"])
			self.id=post["id"]	 
		else:
			self.id=postID
		self.message=msg
	
	def comment(self, msg):
		print("new comment: ",msg)
		return self.graph.put_object(self.id, "comments", message=msg.encode('utf-8'))
	
	def addListener(self,pattern,callback):
		self.listeners.append((pattern,callback))

	def removeListener(self,pat):
		for (pattern,callback) in self.listeners:
			if (pat == pattern):
				self.listeners.remove((pattern,callback))

	def clearListeners(self):
		self.listeners=[]

	def listen(self):
		if (self.stop == False):
			t = Timer(self.refreshRate, self.listen).start()
		for l in self.listeners:
			comment=self.graph.get_object(self.id+"/comments", offset=self.offset)
			data=comment['data']
			for d in data:			
				print("Read comment: ",d['message'])
				self.offset = self.offset+1
				for (pattern,callback) in self.listeners:			
					if (re.search(pattern, string.lower(d['message'])) != None):
						callback(self, pattern, d) 			


	

