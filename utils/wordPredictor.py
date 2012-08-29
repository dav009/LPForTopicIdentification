#SVM linear predictor for words
#given a set of words predict whether a word K is likely to appear or not

from svmutil import *
from IO.data import Instance
from copy import deepcopy

class wordPredictor:

	#training set: [ [dimension1,dimension2...] [dimension1,dimension2...] ]
	#training labels [ labelOfInstance1, 		 labelOfInstance2 ]
	#trains an svm classifier for the given training set and training labels
	def __init__(self,trainingSet,trainingLabels):
		self.trainingSet=trainingSet
		self.trainingLabels=trainingLabels
		prob = svm_problem( trainingLabels,trainingSet)
		
		#actual classifier
		self.predictor=svm_train(prob, '-t 1 -c 2 -g 1.2 -d 5')

	#instance is an array [dimension1, dimension2..]
	#predicts the label for an instance
	def predict(self,instance):
		predicted_labels, _, _= svm_predict([1],[instance],self.predictor)
		return predicted_labels

#intances= set of instances
#setOfLabels= set of labels
#trains N classifiers for predicting each of the labels in SetOfLabels
#returns a dictionary. Key: word, value: wordPredictor
def trainSVMPredictoForLabels(instanceVectors,setOfLabels,matrix):
	dictionaryOfPredictors={}
	count=0
	for label in setOfLabels:

		print "training predictor for:"+label
		print str(count+1) + "-out of-"+ str(len(setOfLabels))
		count=count+1
		trainingSet=[]
		trainingLabels=[]
		for i in range(0,len(instanceVectors)):
			instance=instanceVectors[i]
			currentLabel=instance.triple['label']
			if label==currentLabel:
				trainingLabels.append(1.0)
			else:
				trainingLabels.append(0.0)

			trainingSet.append(matrix[i])
		dictionaryOfPredictors[label]=wordPredictor(trainingSet,trainingLabels)
		rightPredictions=0
		for i in range(0,len(instanceVectors)):
			instance=instanceVectors[i]
			currentLabel=instance.triple['label']


			prediction=dictionaryOfPredictors[label].predict(matrix[i])[0]
			if label==currentLabel:
				
				#print "positive (?) prediction: "+ str(prediction)
				if(1.0==prediction):
					rightPredictions=rightPredictions+1
			else:
				#print "negative (?) prediction: "+ str(prediction)
				if(0.0==prediction):
					rightPredictions=rightPredictions+1
		print "***********************presition***:"+str(rightPredictions/(len(instanceVectors)*1.0))
	return dictionaryOfPredictors


#intances= set of instances
#setOfWords= words for which a classifier should be trained
#trains N classifiers for predicting each of the words in SetOfWords
#returns a dictionary. Key: word, value: wordPredictor
#vocabulary: list of words in which the vectors of the instances will be generated
def trainPredictors(instances,setOfWords,vocabulary):
	dictionaryOfPredictors={}

	#calculating a predictor
	count=0
	for keyWord in setOfWords:

		print "training predictor for:"+keyWord
		print str(count+1) + "-out of-"+ str(len(setOfWords))
		count=count+1

		vocabulary_temp=deepcopy(vocabulary)
		trainingSet=[]
		trainingLabels=[]


		if(keyWord in vocabulary):
			vocabulary_temp.remove(keyWord)

		for instance in instances:
			if instance.getFrecuencyTable().get(keyWord)>0.0:
				trainingLabels.append(1.0)
			else:
				trainingLabels.append(0.0)

			trainingSet.append(instance.getVectorRepresentation(vocabulary_temp))


		dictionaryOfPredictors[keyWord]=wordPredictor(trainingSet,trainingLabels)

		for instance in instances:
			if instance.getFrecuencyTable().get(keyWord)>0.0:
				print "positive (?) prediction: "+ str(dictionaryOfPredictors[keyWord].predict(instance.getVectorRepresentation(vocabulary_temp)))
			else:
				print "negative (?) prediction: "+ str(dictionaryOfPredictors[keyWord].predict(instance.getVectorRepresentation(vocabulary_temp)))




	return dictionaryOfPredictors



#just for testing
if __name__=="__main__":
	trainingSet=[[0,1,2], [0,1,0], [0,10,2] ]
	labels=[ 1,2,1]
	predictor1=wordPredictor(trainingSet,labels)
	
	label= predictor1.predict([0,1,0])
	print "predicted label"
	print label
