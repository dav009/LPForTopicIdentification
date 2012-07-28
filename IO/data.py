import processing.cleaning

class Instance:

	def __init__(self,triple):
		self.triple=triple

	#change the message in the triple,cleaning it
	def cleanMessage(self):
		#do stemming
		self.triple['message']=processing.cleaning.stemming(self.triple['message'])
		
		#remove stopwords,make words lowercase
		self.triple['message']=processing.cleaning.removeStopWords(self.triple['message'])
		
		return 1

	#retunrs a dictionary with the number of times each term appears in the message
	def getFrecuencyTable(self):
		return 1

	#compares this object with another instance of Instance
	def compare(self,b):
		#apply some similarity measure (cosine)
		return 1

	
		
		
