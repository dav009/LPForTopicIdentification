#author: David Przybilla
#date: July 2012
#this file is the main of the app

from IO.csvReader import readCSV
from IO.data import Instance

def main():
	
	#Read the file and convert triples into objects
	
	#read file with messages
	listOfTriples=readCSV("/home/attickid/LPproject/LPForTopicIdentification/Data/terra.csv")
	
	listOfData=[]
	#convert the triples to objects
	for triple in listOfTriples:
		listOfData.append(Instance(triple))
		
	#do cleaning
	for instance in listOfData:
		#clean message
		instance.cleanMessage()
		
		

	#call the feature extration

	#measure the similarities

	#define the graph

	#call JUNTO

	#asses output


main()

