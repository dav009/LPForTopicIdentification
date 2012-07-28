#Allows 
#1.stemming
#2.removing stop words
#3.cast to lowercase
#4.get frecuency tables.
#5.generating JUNTO graph format
import os
from nltk.corpus import stopwords

#PATH OF TREETRAGGER
TREE_TAGGER_PATH="/home/attickid/LPproject/LPForTopicIdentification/processing/stemming/treeTagger/cmd/"

#given a message returns a message steamed
def stemming(message):
	newMessage=""
	
	os.system('echo '+message+ ' | '+TREE_TAGGER_PATH+'tree-tagger-spanish-utf8 >temp');
	pos=open("temp",'r')	
	for line in pos.readlines():
				postagging=line.split("\t")
				
				#in case it is Verb we want to get the infinitive representation to make presentation less sparce
				if(postagging[1] in ["VLfin","VLger","VLinf","VLadj","VBZ","VB","ADJ","VMadj","VLadj","VLger","VLinf","VCLIinf","VCLIger","VMfin","VSfin","VSger"] and not(postagging[2].strip()=="<unknown>")):
					newMessage=newMessage+" "+postagging[2].strip()
			
				else:
					newMessage=newMessage+" "+postagging[0].strip()
	
	return newMessage

#given a text returns a version of text where all the stop words are removed (cast the text into lowercase)
def removeStopWords(message):
	newMessage=""
	words=message.split(" ")
	
	forbiddenList=[",",".","!","?"]
	#replaces the word of forbiddenlsit
	for word in forbiddenList:
		message=message.replace(word,"");
	#look for stopwords and ignore them
	#converts the words to lower case
	for word in words:
		if ((not word in stopwords.words('spanish'))):
			newMessage=newMessage+" "+word.lower()
	return newMessage

#just for testing
if __name__=="__main__":
	stemming('tu vives bien')


