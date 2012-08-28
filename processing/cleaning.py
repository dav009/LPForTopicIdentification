#Allows 
#1.stemming
#2.removing stop words
#3.cast to lowercase
#4.get frecuency tables.
#5.generating JUNTO graph format
import os
import unicodedata
import re
from nltk.corpus import stopwords

#PATH OF TREETRAGGER
TREE_TAGGER_PATH="/home/attickid/LPproject/LPForTopicIdentification/processing/stemming/treeTagger/cmd/"


#remove accents
def removeAccents(message):
	returnMessage=""
	for word in message.split(" "):
		returnMessage=returnMessage+" "+removeAccentsFromWord(word).decode('utf-8')

	print "cleaned accents"
	print returnMessage
	return returnMessage.strip()


def removeAccentsFromWord(word):
	return unicodedata.normalize('NFKD',word.decode('utf-8')).encode('ASCII', 'ignore').decode()

#given a message returns a message steamed
def stemming(message):
	newMessage=""

	message=message.replace("(",'')
	message=message.replace(")",'')
	message=message.replace("\"",'')
	message=message.replace(":",'')

	os.system('echo '+message+ ' | '+TREE_TAGGER_PATH+'tree-tagger-spanish-utf8 >temp');
	pos=open("temp",'r')	
	for line in pos.readlines():
				postagging=line.split("\t")
				
				#in case it is Verb we want to get the infinitive representation to make presentation less sparce
				if(postagging[1] in ["VLfin","VLger","VLinf","VLadj","VBZ","VB","ADJ","VMadj","VLadj","VLger","VLinf","VCLIinf","VCLIger","VMfin","VSfin","VSger"] and not(postagging[2].strip()=="<unknown>")):
					newMessage=newMessage+" "+postagging[2].strip()
			
				else:
					if(postagging[1] in ["NC","NMEA","NP"] ):
						newMessage=newMessage+" "+postagging[0].strip()
	
	return newMessage

#given a text returns a version of text where all the stop words are removed (cast the text into lowercase)
def removeStopWords(message):

	#look for patterns of twitter noise
	 #pattern for mentions
	p = re.compile( '@(\w)+')
	message=p.sub("",message)

	 #pattern for laughs
	p = re.compile( 'jaja(ja)*')
	message=p.sub("",message)

	p = re.compile( 'jiji(ji)*')
	message=p.sub("",message)

	p = re.compile( 'jeje(je)*')
	message=p.sub("",message)

	p = re.compile( 'haha(ha)*')
	message=p.sub("",message)

	p = re.compile( 'w(w)*(o)+(w)*w')
	message=p.sub("",message)

	p = re.compile( '|')
	message=p.sub("",message)

	newMessage=""
	
	
	forbiddenList=["|",".","!","?","\n","\t","(",")",',',"me","le","jaja","jeje","wow","jiji","haha","te","yo","rt","rt:"]
	#replaces the word of forbiddenlsit
	for word in forbiddenList:
		message=message.replace(word,'');
	#look for stopwords and ignore them
	#converts the words to lower case

	words=message.split(" ")

	for word in words:
		if ((not word in stopwords.words('spanish')) and not(word==" ")):
			newMessage=newMessage+" "+word.lower()


	
	return newMessage





#just for testing
if __name__=="__main__":
	stemming('tu vives bien')





