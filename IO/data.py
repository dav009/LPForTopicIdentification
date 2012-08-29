import processing.cleaning
from math import log
from utils.frencuencyTable import frecuencyTable
from  Queue import PriorityQueue
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

		#remove acceptns
		self.triple['message']=processing.cleaning.removeAccents(self.triple['message'])
		
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

	#returns a vector representation of this message
	#keys are a list of words which will be used for the vector representation
	def getVectorRepresentation(self,keys):
		vector=[]
		for key in keys:
			value=self.tableOfFrequencies.get(key)
			vector.append(value)
		return vector



#Auxialiry Functions

#get sets of Words per Label
#given a list of Instance bojects it returns per each label,the list of words common to that label with high frequency
#returns a list of Set
#input: setOfWords : the vocabulary
#		listOfinstances: list of messages
# 		type: type of grouping which want to be achieved
#processing: iterate for every word in the vocabulary looking its predictve structure with respect to each label
#output: list of of [word,label,pmi]      
def getSetOfWordsPerLabel(setOfLabels,setOfWords,listOfInstances,type):

	returnList={}

	#initialize the priorityQueues
	for label in setOfLabels:
		returnList[label]=PriorityQueue()


	if(type=="highFrequency"):
		#get words with highfreqenquecny per label
		print "getting words with high freqeuncy group by label"
	if(type=="PMI"):
		#get words that are the best predictors for a label 

		print "getting words with high freqeuncy group by PMI"

		for label in setOfLabels:
			
			for word in setOfWords:
				triple={}
				#how many times word-label have been seen together
				labelWordCount=0.0
				#how many times a word has been seen in the instances
				wordCount=0.0
				#how many times the label has been seen in the instances
				labelCount=0.0

				numberOfInstances=0.0

				for instance in listOfInstances:
					numberOfInstances=numberOfInstances+1.0
					if(instance.getFrecuencyTable().get(word)>0 and instance.triple['label']==label):
						labelWordCount=labelWordCount+1.0
					if(instance.triple['label']==label):
						labelCount=labelCount+1.0
					if(instance.getFrecuencyTable().get(word)>0):
						wordCount=wordCount+1.0
				triple['word']=word
				triple['label']=label
				
				pmi=labelWordCount/(1.0*numberOfInstances)
				probOfLabel=(labelCount)/numberOfInstances
				probOfWord=(wordCount)/numberOfInstances
				pmi=pmi/(probOfLabel*probOfWord)
				print str(pmi)+" - log"
				if(labelWordCount>0):
					print str(pmi)
					print str(labelWordCount/(1.0*labelCount))
					print str(log(labelWordCount/(1.0*labelCount)))
					triple['pmi']=log(pmi)/(-1* log(labelWordCount/(1.0*numberOfInstances)) )
				else:
					triple['pmi']=-1
				returnList[label].put((1-triple['pmi'],triple))
	return returnList


		
		
