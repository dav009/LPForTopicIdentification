#author: David Przybilla
#date: July 2012
#this file is the main of the app

from IO.csvReader import readCSV
from IO.data import Instance
from sets import Set
import numpy as np
from processing.LatentSemantic import *

def main():
	
	#Read the file and convert triples into objects
	
	#read file with messages
	listOfTriples=readCSV("/home/attickid/LPproject/LPForTopicIdentification/Data/terra2short.csv")
	
	listOfData=[]
	#convert the triples to objects
	for triple in listOfTriples:
		listOfData.append(Instance(triple))
		
	#stores the vocabulry  of the docs
	setOfWords=Set()
	for instance in listOfData:
		#clean message
		instance.cleanMessage()
		instance.measureFrequencies()
		#gathers the frequencies in each message
		#add each word to the setOfWords(vocabulary)
		currentVocabulary=instance.getFrecuencyTable().getKeys()
		for v in currentVocabulary:
			setOfWords.add(v)

	#creates the vector for each instance
	instanceVectors=[]
	for instance in listOfData:
		for word in setOfWords:
			instance.vector.append(instance.getFrecuencyTable().get(word))
		instanceVectors.append(instance.vector)
			
		
		
	

	#SVD
	matrix =np.matrix(instanceVectors)
	matrix=	tfidfTransform(matrix)
	matrixLSA=svdDimensionalityReduction(matrix,1)

	print matrixLSA

	#measure the similarities
	similarities={}
	for i in range(0,len(instanceVectors):
		for j in range(i+1,len(instanceVectors):
			similarities[i+'_'+j]=distance(matrixLSA[i],matrixLSA[j],'cosine')

	#define the graph

	#call JUNTO

	#asses output


main()

