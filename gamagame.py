#!/usr/bin/python
import facebook
import random
import fbot
import time
from threading import Timer
import string

class GamaGame:
	def __init__(self,g): 
		self.maxTime=5 * 60
		self.timeout=None
		self.currentQuestion=None
		self.remainingAnswers=0
		self.hits=[]
		self.interval=30
		self.graph=g
		self.questions=self.getQuestions()
	
	def getQuestions(self):
		questions=[]
		f=open("gamagame.hsh", "r")
		question=""
		i=0		
		for line in f.readlines():
			if (i%2 == 0):
				question=string.strip(line)
			else:
				answers=string.split(string.strip(string.lower(line)),'|')
				questions.append((question, answers));
			i=i+1		
		return questions

	def startGame(self):
		self.hits={}
		self.currentQuestion=random.choice(self.questions)
		(question,answers)=self.currentQuestion
		self.remainingAnswers=len(answers)
		self.post=fbot.fbotPost(self.graph, "thegamagame", str((self.maxTime/60))+" mins: "+question+"?")
		for ans in answers:
			self.post.addListener(ans, self.onHit)
		self.timeout=Timer(self.maxTime, self.endGame)
		self.timeout.start()
		self.post.listen()
		
	def onHit(self, post, pattern, data):
		post.removeListener(pattern)
		self.hits[pattern]=data['from']
		self.remainingAnswers=self.remainingAnswers-1
		post.comment(data['from']['name']+" answered \""+pattern+"\" correctly!!!")
		if (self.remainingAnswers == 0):
			self.endGame()
		else:
			post.comment(str(self.remainingAnswers)+" remaining answers")			
	
	def endGame(self):
		self.post.clearListeners()
		self.post.stop=True
		self.timeout.cancel()
		(q,answers) = self.currentQuestion
		for ans in answers:
			if ans not in self.hits.keys():
				self.post.comment("Nobody answered "+ans)
			
		self.post.comment("END OF THE GAME! Next in "+str(self.interval)+" seconds")	
		time.sleep(self.interval)
		self.startGame()

fConf = open("config_access_token")
ACCESS_TOKEN = string.strip(fConf.read())
graph = facebook.GraphAPI(ACCESS_TOKEN)
game = GamaGame(graph)
game.startGame()

