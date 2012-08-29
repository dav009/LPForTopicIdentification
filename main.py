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
from utils.wordPredictor import trainSVMPredictoForLabels
from copy import deepcopy
from utils.frencuencyTable import frecuencyTable



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

#given a path to a file and a list of vectors it generates a junto graph
def createJuntoGraph(path,instanceVectors,matrixLSA):
	#creates a file with the graph description for JUNTO to use
	graphFile=open(path,'w')
	juntoGraphFileContent=""

	for i in range(0,len(instanceVectors)):
		for j in range(i+1,len(instanceVectors)):
			distanceValue=distance(matrixLSA[i],matrixLSA[j],'cosine')
			juntoGraphFileContent=juntoGraphFileContent+str(i)+"\t"+str(j)+"\t"+str(distanceValue)+"\n"
	graphFile.write(juntoGraphFileContent)

def trainSupervisedSVM():

	#table frquencuency of all the words in the messages
	frecuencies=frecuencyTable()
	
	#Read the file and convert triples into objects
	
	#read file with messages
	listOfTriples=readCSV("Data/terraReducedTest.csv")
	
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


		#clean message
		instance.cleanMessage()
		instance.measureFrequencies()

		if(instance.triple['label']!=None and instance.triple['label']!=''):
			setOfLabels.add(instance.triple['label'])

		print setOfLabels
		#gathers the frequencies in each message
		#add each word to the setOfWords(vocabulary)
		currentVocabulary=instance.getFrecuencyTable().getKeys()
		for v in currentVocabulary:
			setOfWords.add(v)

		for word in instance.triple['message'].split(" "):
			frecuencies.add(word)

	listOfWordsByValue=frecuencies.sort_by_value()
	print "words by frequencie---"
	for wordd in listOfWordsByValue:
		print wordd
	print "--------------------------"

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

	#of dimensions
	numberOfDimensions=1000000000000000000000000000000000000000000
	for Keyqueue in listOfPMI.keys():
		queue=listOfPMI[Keyqueue]
		currentCount=0
		while not queue.empty() and currentCount<numberOfDimensions:
			pmi=queue.get()[1]
			
			if(pmi['pmi']>0.2): #not taking into account the pmi
				#print pmi['word']+"--"+str(pmi['pmi'])+"--"+pmi['label']
				currentCount=currentCount+1
				setOfSelectedWords.add(pmi['word'])


	#train a set of Classifiers for words
	print "training classifiers"
	#setOfClassifiers=trainPredictors(listOfData,setOfSelectedWords,setOfWords)
	

	#once the classifiers are trained get the

	#creates a file for fpgrowth
	contentFileForFPGrowth=""

	#creates the vector for each instance
	print "creating vectors for each message"
	instanceVectors=[]
	for instance in listOfData:
		#for word in setOfWords: #when generating vectors with all the words in the vocabulary
		for word in setOfSelectedWords: #when generating vectors with just the words above the MPI threshold
			#using linear classs
			#if(instance.getFrecuencyTable().get(word)*1.0>100.0):
			#	instance.vector.append(instance.getFrecuencyTable().get(word)*1.0)
			#else:
			#	vocabulary_temp=deepcopy(setOfWords)
			#	if(word in setOfWords):
			#		vocabulary_temp.remove(word)
			#	vectorRepresentation=instance.getVectorRepresentation(vocabulary_temp)
			#	label=setOfClassifiers[word].predict(vectorRepresentation)
			#	if(label[0]>0.0):
			#		print "calculated label: "+str(label)
			#	instance.vector.append(label[0])
			#/using linearclass
			instance.vector.append(instance.getFrecuencyTable().get(word)*1.0) #if prediction does not matter
			if(instance.getFrecuencyTable().get(word)>0):
				contentFileForFPGrowth=contentFileForFPGrowth+" "+word
		contentFileForFPGrowth=contentFileForFPGrowth+"\n"		
		instanceVectors.append(instance.vector)

		FPgrowthFile=open('fpgrowthdata','w')
		FPgrowthFile.write(contentFileForFPGrowth)


	

			
		
		
	

	#SVD
	matrix =np.matrix(instanceVectors)
	print "calculating tf-idf"
	matrix=	tfidfTransform(instanceVectors)
	print "calculatin svd"
	matrixLSA=matrix
	#matrixLSA=svdDimensionalityReduction(matrix,1)

	#print matrixLSA

	print "calculating the graph files for Junto"
	


	#creates a junt graph
	#createJuntoGraph('input_graph',instaceVectors,matrixLSA)
	



	#trains a classifier for a label on all the data
	#trainSVMPredictoForLabels(listOfData,setOfLabels,matrixLSA)
	
	currentNumberOfSeedsPerLabel={}
	for key in setOfLabels:
		currentNumberOfSeedsPerLabel[key]=0



	#this defines the number of seeds(annotated data for the algorithm)
	
	
	currentNumberOfSeedsPerLabel={}
	for key in setOfLabels:
		currentNumberOfSeedsPerLabel[key]=0

	#there should be an equal number of seeds for each label
	percentage=0.1
	numberOfSeeds=len(instanceVectors)*percentage
	currentNumberOfSeeds=0

	numberOfSeedsPerLabel=math.floor(numberOfSeeds/(1.0*len(setOfLabels)))
	numberOfSeeds=numberOfSeedsPerLabel*len(setOfLabels)

	#creates the gold_labels for Junto( the instnaces whose label is known)
	#seed files refer to those instances which label is already given
	seedFileContent=""
	seedFile=open("seeds",'w')

	#training set of instances
	trainingListOfdata=[]
	#training set of vectors
	trainingMatrix=[]

	#testData
	testListOfdata=[]
	testMatrix=[]


	#gold file refers to the goldstandard towards the perfomrance is measureed
	goldFileContent=""
	goldFile=open("gold_labels",'w')
	counter_=0
	SetOfSeeds=Set()

	for instance in listOfData:
		if ( (not instance.triple['label']=='') and (not instance.triple['label']==None) ):
			#if the instance is between the first 1000 then it is  a seed otherwise it is test
			if(currentNumberOfSeedsPerLabel[instance.triple['label']]<numberOfSeedsPerLabel and  not instance.triple['message'] in SetOfSeeds):
				seedFileContent=seedFileContent+str(instance.triple['id'])+"\t"+instance.triple['label']+"\t"+"1.0\n"
				currentNumberOfSeedsPerLabel[instance.triple['label']]=currentNumberOfSeedsPerLabel[instance.triple['label']]+1
				trainingListOfdata.append(instance)
				trainingMatrix.append(matrixLSA[counter_])
				SetOfSeeds.add(instance.triple['message'])
			else:
				goldFileContent=goldFileContent+str(instance.triple['id'])+"\t"+instance.triple['label']+"\t"+"1.0\n"
				testListOfdata.append(instance)
				testMatrix.append(matrixLSA[counter_])
		counter_=counter_+1

	seedFile.write(seedFileContent)
	goldFile.write(goldFileContent)


	#train an svm classifier for the given samples
	print "len of training data:"+str(len(trainingListOfdata))
	listOfClassifiers=trainSVMPredictoForLabels(trainingListOfdata,setOfLabels,trainingMatrix)
	countOfRightClassifications=0
	countOfPredictions=0
	for i in range(0, len(testListOfdata)):
		for label in setOfLabels:
			
			
			prediction=listOfClassifiers[label].predict(testMatrix[i])[0]
			print "predicttion of:: "+label+":"+str(prediction)+"__real:"+testListOfdata[i].triple['label']
			countOfPredictions=countOfPredictions+1
			if(prediction==1.0):
				
				print "predicted:: "+label+"__real:"+testListOfdata[i].triple['label']
				if(label==testListOfdata[i].triple['label']):
					countOfRightClassifications=countOfRightClassifications+1
			else:
				
				print "predicted:: "+label+"__real:"+testListOfdata[i].triple['label']
				if(label!=testListOfdata[i].triple['label']):
					countOfRightClassifications=countOfRightClassifications+1

	print "len of testdata:"+str(len(testListOfdata))
	print "right class:"+str(countOfRightClassifications)
	print "number of predctions:"+str(countOfPredictions)
	print "accuracy: "+str(countOfRightClassifications/(countOfPredictions*1.0))


	#gold labels


	#call JUNTO

	#asses output

def  justGenerateSeeds(percentage):

	setOfLabels=Set()

	#this defines the number of seeds(annotated data for the algorithm)
	percentageOfSeeds=percentage
	#read file with messages
	listOfTriples=readCSV("Data/sonyReduced.csv")
	
	instanceVectors=[]
	#convert the triples to objects
	for triple in listOfTriples:
		instanceVectors.append(Instance(triple))
		setOfLabels.add(triple['label'])

	numberOfSeeds=len(instanceVectors)*percentage
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
	seedFile=open("seeds_"+str(percentage),'w')

	SetOfSeeds=Set()
	
	for instance in instanceVectors:
		if ( (not instance.triple['label']=='') and (not instance.triple['label']==None) and not instance.triple['message'] in SetOfSeeds):
			#if the instance is between the first 1000 then it is  a seed otherwise it is test
			if(currentNumberOfSeedsPerLabel[instance.triple['label']]<numberOfSeedsPerLabel):
				SetOfSeeds.add(instance.triple['message'])
				seedFileContent=seedFileContent+str(instance.triple['id'])+"\t"+instance.triple['label']+"\t"+"1.0\n"
				currentNumberOfSeedsPerLabel[instance.triple['label']]=currentNumberOfSeedsPerLabel[instance.triple['label']]+1
	seedFile.write(seedFileContent)

	return ()
	


def trainSemisupervisedSVM():
	print "training semi-supervised"
	#table frquencuency of all the words in the messages
	frecuencies=frecuencyTable()
	
	#Read the file and convert triples into objects
	
	#read file with messages
	listOfTriples=readCSV("Data/terraReduced.csv")
	
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


		#clean message
		instance.cleanMessage()
		instance.measureFrequencies()

		if(instance.triple['label']!=None and instance.triple['label']!=''):
			setOfLabels.add(instance.triple['label'])

		print setOfLabels
		#gathers the frequencies in each message
		#add each word to the setOfWords(vocabulary)
		currentVocabulary=instance.getFrecuencyTable().getKeys()
		for v in currentVocabulary:
			setOfWords.add(v)

		for word in instance.triple['message'].split(" "):
			frecuencies.add(word)

	listOfWordsByValue=frecuencies.sort_by_value()
	print "words by frequencie---"
	for wordd in listOfWordsByValue:
		print wordd
	print "--------------------------"

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

	#of dimensions
	numberOfDimensions=1000000000000000000000000000000000000000000
	for Keyqueue in listOfPMI.keys():
		queue=listOfPMI[Keyqueue]
		currentCount=0
		while not queue.empty() and currentCount<numberOfDimensions:
			pmi=queue.get()[1]
			
			if(pmi['pmi']>0.2): #not taking into account the pmi
				#print pmi['word']+"--"+str(pmi['pmi'])+"--"+pmi['label']
				currentCount=currentCount+1
				setOfSelectedWords.add(pmi['word'])


	#train a set of Classifiers for words

	numberOfSelectedWords=len(setOfSelectedWords)
	#words used as features
	setOfWords1=Set()
	#words to predict
	setOfWords2=Set()

	index=0
	for word in setOfSelectedWords:
		if(index%2==0):
			setOfWords1.add(word)
		else:
			setOfWords2.add(word)
		index=index+1



	print "training classifiers"
	# the vector for training will be measured using: instance.getVectorRepresentation(setOfWords1)
	
		#this defines the number of seeds(annotated data for the algorithm)
	
	
	currentNumberOfSeedsPerLabel={}
	for key in setOfLabels:
		currentNumberOfSeedsPerLabel[key]=0

	#there should be an equal number of seeds for each label
	percentage=0.1
	numberOfSeeds=len(listOfData)*percentage
	currentNumberOfSeeds=0

	numberOfSeedsPerLabel=math.floor(numberOfSeeds/(1.0*len(setOfLabels)))
	numberOfSeeds=numberOfSeedsPerLabel*len(setOfLabels)
	listForAuxiliaryTraining=[]
	SetOfSeeds2=Set()
	for instance in listOfData:
		if ( (not instance.triple['label']=='') and (not instance.triple['label']==None) ):
			#if the instance is between the first 1000 then it is  a seed otherwise it is test
			if(currentNumberOfSeedsPerLabel[instance.triple['label']]<numberOfSeedsPerLabel and  not instance.triple['message'] in SetOfSeeds2):
				currentNumberOfSeedsPerLabel[instance.triple['label']]=currentNumberOfSeedsPerLabel[instance.triple['label']]+1
				SetOfSeeds2.add(instance.triple['message'])
			else:
				listForAuxiliaryTraining.append(instance)
		

	setOfClassifiers=trainPredictors(listForAuxiliaryTraining,setOfSelectedWords,setOfWords)

	#once the classifiers are trained get the

	#creates a file for fpgrowth
	contentFileForFPGrowth=""

	#creates the vector for each instance
	print "creating vectors for each message"
	instanceVectors=[]
	for instance in listOfData:
		#for word in setOfWords: #when generating vectors with all the words in the vocabulary
		for word in setOfSelectedWords: #when generating vectors with just the words above the MPI threshold
			#using linear classs
			if(not instance.triple['message'] in SetOfSeeds2):
				instance.vector.append(instance.getFrecuencyTable().get(word)*1.0)
			else:

				if(instance.getFrecuencyTable().get(word)*1.0>100.0):
					instance.vector.append(instance.getFrecuencyTable().get(word)*1.0)
				else:
					vocabulary_temp=deepcopy(setOfWords)
					if(word in setOfWords):
						vocabulary_temp.remove(word)
					vectorRepresentation=instance.getVectorRepresentation(vocabulary_temp)
					label=setOfClassifiers[word].predict(vectorRepresentation)
					instance.vector.append(label[0])
			#/using linearclass
			#instance.vector.append(instance.getFrecuencyTable().get(word)*1.0) #if prediction does not matter
			if(instance.getFrecuencyTable().get(word)>0):
				contentFileForFPGrowth=contentFileForFPGrowth+" "+word
		contentFileForFPGrowth=contentFileForFPGrowth+"\n"		
		instanceVectors.append(instance.vector)

		FPgrowthFile=open('fpgrowthdata','w')
		FPgrowthFile.write(contentFileForFPGrowth)


	

			
		
		
	

	#SVD
	matrix =np.matrix(instanceVectors)
	print "calculating tf-idf"
	matrix=	tfidfTransform(instanceVectors)
	print "calculatin svd"
	matrixLSA=matrix
	#matrixLSA=svdDimensionalityReduction(matrix,1)

	#print matrixLSA

	print "calculating the graph files for Junto"
	


	#creates a junt graph
	#createJuntoGraph('input_graph',instaceVectors,matrixLSA)
	



	#trains a classifier for a label on all the data
	#trainSVMPredictoForLabels(listOfData,setOfLabels,matrixLSA)
	
	



	#this defines the number of seeds(annotated data for the algorithm)
	
	
	currentNumberOfSeedsPerLabel={}
	for key in setOfLabels:
		currentNumberOfSeedsPerLabel[key]=0

	
	#creates the gold_labels for Junto( the instnaces whose label is known)
	#seed files refer to those instances which label is already given
	seedFileContent=""
	seedFile=open("seeds",'w')

	#training set of instances
	trainingListOfdata=[]
	#training set of vectors
	trainingMatrix=[]

	#testData
	testListOfdata=[]
	testMatrix=[]


	#gold file refers to the goldstandard towards the perfomrance is measureed
	goldFileContent=""
	goldFile=open("gold_labels",'w')
	counter_=0
	SetOfSeeds=Set()

	for instance in listOfData:
		if ( (not instance.triple['label']=='') and (not instance.triple['label']==None) ):
			#if the instance is between the first 1000 then it is  a seed otherwise it is test
			if(currentNumberOfSeedsPerLabel[instance.triple['label']]<numberOfSeedsPerLabel and  not instance.triple['message'] in SetOfSeeds):
				seedFileContent=seedFileContent+str(instance.triple['id'])+"\t"+instance.triple['label']+"\t"+"1.0\n"
				currentNumberOfSeedsPerLabel[instance.triple['label']]=currentNumberOfSeedsPerLabel[instance.triple['label']]+1
				trainingListOfdata.append(instance)
				trainingMatrix.append(matrixLSA[counter_])
				SetOfSeeds.add(instance.triple['message'])
			else:
				goldFileContent=goldFileContent+str(instance.triple['id'])+"\t"+instance.triple['label']+"\t"+"1.0\n"
				testListOfdata.append(instance)
				testMatrix.append(matrixLSA[counter_])
		counter_=counter_+1

	seedFile.write(seedFileContent)
	goldFile.write(goldFileContent)


	#train an svm classifier for the given samples
	print "len of training data:"+str(len(trainingListOfdata))
	listOfClassifiers=trainSVMPredictoForLabels(trainingListOfdata,setOfLabels,trainingMatrix)
	countOfRightClassifications=0
	countOfPredictions=0
	for i in range(0, len(testListOfdata)):
		for label in setOfLabels:
			
			
			prediction=listOfClassifiers[label].predict(testMatrix[i])[0]
			print "predicttion of:: "+label+":"+str(prediction)+"__real:"+testListOfdata[i].triple['label']
			countOfPredictions=countOfPredictions+1
			if(prediction==1.0):
				
				print "predicted:: "+label+"__real:"+testListOfdata[i].triple['label']
				if(label==testListOfdata[i].triple['label']):
					countOfRightClassifications=countOfRightClassifications+1
			else:
				
				print "predicted:: "+label+"__real:"+testListOfdata[i].triple['label']
				if(label!=testListOfdata[i].triple['label']):
					countOfRightClassifications=countOfRightClassifications+1

	print "len of testdata:"+str(len(testListOfdata))
	print "right class:"+str(countOfRightClassifications)
	print "number of predctions:"+str(countOfPredictions)
	print "accuracy: "+str(countOfRightClassifications/(countOfPredictions*1.0))




#listOfPercentages=[0.1,0.2,0.3,0.5,0.8]
#for percentage in listOfPercentages:
#	justGenerateSeeds(percentage)


#call for training a supervised SVM
#trainSupervisedSVM()

#call for training semisupervisd
trainSemisupervisedSVM()

