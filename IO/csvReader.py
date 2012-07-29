#author: David Przybilla
#date: July 2012
#read a csv file

import csv

#given a path to a csv file returns a list of triples (message,label,polarity)
def readCSV(path):
	dataReader = csv.reader(open(path, 'rb'), delimiter=',', quotechar='"')
	#list Of triples to return	
	listOfTriples=[]

	#just reads the name of the fields
	#find their indexes
	currentIndex=0
	indexMessage=-1
	indexLabel1=-1
	indexLabel2=-1
	indexPolarity=-1
	row_=dataReader.next()
	#find the index of the desired fields
	for field in row_:
		if field=="Mensaje":
			indexMessage=currentIndex
		if field=="Categoria 1":
			indexLabel1=currentIndex
		if field=="Categoria 2":
			indexLabel2=currentIndex
		if field=="Tono":
			indexPolarity=currentIndex
		currentIndex=currentIndex+1

	counter=0
	for row in dataReader:
		triple={}
		#get the data from csv file		
		triple['message']=row[indexMessage]
		triple['id']=counter
		counter=counter+1
		
		if(row[indexLabel1]==''):
			triple['label']=row[indexLabel2]
		else:
			triple['label']=row[indexLabel1]
		triple['polarity']=row[indexPolarity]

		listOfTriples.append(triple)
		print triple

	return listOfTriples

	
		



#just for testing
if __name__=="__main__":
	readCSV("/home/attickid/LPproject/LPForTopicIdentification/Data/terra.csv")


