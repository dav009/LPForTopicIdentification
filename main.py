#author: David Przybilla
#date: July 2012
#this file is the main of the app

from IO.csvReader import readCSV
from IO.data import Instance
from sets import Set
import numpy as np
from processing.LatentSemantic import *
from math import sqrt

#measures the distance among two vectors
def distance(v1,v2,similarityMeasure):
		result=0.0
		if(similarityMeasure=="euclidean"):
				for index in range(0,len(v1)):
						result=result+((v1[index]-v2[index])**2)
				return sqrt(result)

def main():
	
	#Read the file and convert triples into objects
	
	#read file with messages
	listOfTriples=readCSV("/home/attickid/LPproject/LPForTopicIdentification/Data/terraReduced.csv")
	
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
	#creates a file with the graph description for JUNTO to use
	graphFile=open("junto_graph_messages",'w')
	juntoGraphFileContent=""

	for i in range(0,len(instanceVectors)):
		for j in range(i+1,len(instanceVectors)):
			distanceValue=distance(matrixLSA[i],matrixLSA[j],'euclidean')
			similarities[str(i)+'_'+str(j)]=distanceValue
			juntoGraphFileContent=juntoGraphFileContent+str(i)+"\t"+str(j)+"\t"+str(distanceValue)+"\n"
	graphFile.write(juntoGraphFileContent)

	#creates the gold_labels for Junto( the instnaces whose label is known)
	goldFileContent=""
	goldFile=open("junto_graph_seeds",'w')
	for instance in listOfData:
		if ( (not instance.triple['label']=='') and (not instance.triple['label']==None)):
			goldFileContent=goldFileContent+str(instance.triple['id'])+"\t"+instance.triple['label']+"\t"+"1.0\n"
	goldFile.write(goldFileContent)


	#call JUNTO

	#asses output


main()

