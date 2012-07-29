import processing.cleaning
from utils.frencuencyTable import frecuencyTable
class Instance:

	def __init__(self,triple):
		self.triple=triple
		self.vector=[]

	#change the message in the triple,cleaning it
	def cleanMessage(self):
		#do stemming
		self.triple['message']=processing.cleaning.stemming(self.triple['message'])
		
		#remove stopwords,make words lowercase
		self.triple['message']=processing.cleaning.removeStopWords(self.triple['message'])
		
		return 1

	#calculates the tableOfFrquencies
	def measureFrequencies(self):
		#creates a new table of frequencies
		self.tableOfFrequencies=frecuencyTable()
		#get the words of the message
		words=self.triple['message'].split(" ");
		#count how many times is each word
		for word in words:
			self.tableOfFrequencies.add(word)

	#retunrs a dictionary with the number of times each term appears in the message
	def getFrecuencyTable(self):
		return self.tableOfFrequencies

	#compares this object with another instance of Instance
	def compare(self,b):
		#apply some similarity measure (cosine)
		return 1

	
		
		
