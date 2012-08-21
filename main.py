#author: David Przybilla
#date: July 2012
#this file is the main of the app

from IO.csvReader import readCSV
from IO.data import Instance
from IO.data import getSetOfWordsPerLabel
from sets import Set
import numpy as np
from processing.LatentSemantic import *
from math import sqrt
from math import floor
from math import cos
from math import degrees
from  Queue import PriorityQueue
from utils.wordPredictor import wordPredictor
from utils.wordPredictor import trainPredictors

#measures the distance among two vectors, test gitplugin5
def distance(v1,v2,similarityMeasure):
		result=0.0
		if(similarityMeasure=="euclidean"):
				for index in range(0,len(v1)):
						result=result+((v1[index]-v2[index])**2)
				return 100.0-sqrt(result)
		if(similarityMeasure=="cosine"):
				denominator=0.0
				numerator=0.0
				sumA=0.0
				sumB=0.0
				for index in range(0,len(v1)):
						numerator=numerator+(v1[index]*v2[index])
						sumA=sumA+(v1[index]**2)
						sumB=sumB+(v2[index]**2)
				denominator=(sqrt(sumA)*sqrt(sumB))
				if(denominator>0.00000000000000000000000000000000000000000000000):
					result=numerator/denominator
				else:
					result=0.0000000000000000000000000000000000000000000000000000000000000000000000000001
				
				
				return result

def main():
	
	#Read the file and convert triples into objects
	
	#read file with messages
	listOfTriples=readCSV("/home/attickid/LPproject/LPForTopicIdentification/Data/sonyReduced.csv")
	
	listOfData=[]
	#convert the triples to objects
	for triple in listOfTriples:
		listOfData.append(Instance(triple))
		
	#stores the vocabulry  of the docs
	setOfWords=Set()
	#stores the set of labels found in the instnaces
	setOfLabels=Set()
	for instance in listOfData:
		print "cleaning: "+str(instance.triple['id'])

		#stores the labels
		if(instance.triple['label']!=None and instance.triple['label']!=''):
			setOfLabels.add(instance.triple['label'])

		#clean message
		instance.cleanMessage()
		instance.measureFrequencies()
		#gathers the frequencies in each message
		#add each word to the setOfWords(vocabulary)
		currentVocabulary=instance.getFrecuencyTable().getKeys()
		for v in currentVocabulary:
			setOfWords.add(v)

	print "looking for PMI"
	#get the instances which are annotated
	listOfAnnotatedData=[]
	listOfUnnanotatedData=[]
	for instance in listOfData:
		if instance.triple['label']!="":
			listOfAnnotatedData.append(instance)
		else:
			listOfUnnanotatedData.append(instance)

	listOfPMI=getSetOfWordsPerLabel(setOfLabels,setOfWords,listOfAnnotatedData,"PMI")
	#the words whose PMI are over a threshold
	setOfSelectedWords=Set()
	for Keyqueue in listOfPMI.keys():
		queue=listOfPMI[Keyqueue]

		while not queue.empty():
			pmi=queue.get()[1]
			
			if(pmi['pmi']>0.3):
				print pmi['word']+"--"+str(pmi['pmi'])+"--"+pmi['label']
				setOfSelectedWords.add(pmi['word'])


	#train a set of Classifiers
	print "training classifiers"
	setOfClassifiers=trainPredictors(listOfData,setOfSelectedWords,setOfWords)
	

	#once the classifiers are trained get the

	#creates the vector for each instance
	print "creating vectors for each message"
	instanceVectors=[]
	for instance in listOfData:
		#for word in setOfWords: #when generating vectors with all the words in the vocabulary
		for word in setOfSelectedWords: #when generating vectors with just the words above the MPI threshold

			if(instance.getFrecuencyTable().get(word)*1.0>0.0):
				instance.vector.append(instance.getFrecuencyTable().get(word)*1.0)
			else:
				vocabulary_temp=setOfWords
				vocabulary_temp.remove(word)
				vectorRepresentation=instance.getVectorRepresentation(vocabulary_temp)
				label=setOfClassifiers[word].predict(vectorRepresentation)
				print "calculated label: "+str(label)
				instance.vector.append(label)
			#instance.vector.append(instance.getFrecuencyTable().get(word)*1.0) #if prediction does not matter
		instanceVectors.append(instance.vector)
			
		
		
	

	#SVD
	matrix =np.matrix(instanceVectors)
	print "calculating tf-idf"
	matrix=	tfidfTransform(instanceVectors)
	print "calculatin svd"
	matrixLSA=matrix
	#matrixLSA=svdDimensionalityReduction(matrix,1)

	print matrixLSA

	print "calculating the graph files for Junto"
	#measure the similarities
	similarities={}
	#creates a file with the graph description for JUNTO to use
	graphFile=open("input_graph",'w')
	juntoGraphFileContent=""

	for i in range(0,len(instanceVectors)):
		for j in range(i+1,len(instanceVectors)):
			distanceValue=distance(matrixLSA[i],matrixLSA[j],'cosine')
			similarities[str(i)+'_'+str(j)]=distanceValue
			
			juntoGraphFileContent=juntoGraphFileContent+str(i)+"\t"+str(j)+"\t"+str(distanceValue)+"\n"
	graphFile.write(juntoGraphFileContent)

	#this defines the number of seeds(annotated data for the algorithm)
	numberOfSeeds=10
	currentNumberOfSeeds=0
	
	currentNumberOfSeedsPerLabel={}
	for key in setOfLabels:
		currentNumberOfSeedsPerLabel[key]=0

	#there should be an equal number of seeds for each label
	numberOfSeedsPerLabel=math.floor(numberOfSeeds/(1.0*len(setOfLabels)))
	numberOfSeeds=numberOfSeedsPerLabel*len(setOfLabels)

	#creates the gold_labels for Junto( the instnaces whose label is known)
	#seed files refer to those instances which label is already given
	seedFileContent=""
	seedFile=open("seeds",'w')
	#gold file refers to the goldstandard towards the perfomrance is measureed
	goldFileContent=""
	goldFile=open("gold_labels",'w')
	for instance in listOfData:
		if ( (not instance.triple['label']=='') and (not instance.triple['label']==None) ):
			#if the instance is between the first 1000 then it is  a seed otherwise it is test
			if(currentNumberOfSeedsPerLabel[instance.triple['label']]<numberOfSeedsPerLabel):
				seedFileContent=seedFileContent+str(instance.triple['id'])+"\t"+instance.triple['label']+"\t"+"1.0\n"
				currentNumberOfSeedsPerLabel[instance.triple['label']]=currentNumberOfSeedsPerLabel[instance.triple['label']]+1
			else:
				goldFileContent=goldFileContent+str(instance.triple['id'])+"\t"+instance.triple['label']+"\t"+"1.0\n"
	seedFile.write(seedFileContent)
	goldFile.write(goldFileContent)

	#gold labels


	#call JUNTO

	#asses output


main()

