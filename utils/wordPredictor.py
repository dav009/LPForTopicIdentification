#SVM linear predictor for words
#given a set of words predict whether a word K is likely to appear or not

from svmutil import *

class wordPredictor:

	#training set: [ [dimension1,dimension2...] [dimension1,dimension2...] ]
	#training labels [ labelOfInstance1, 		 labelOfInstance2 ]
	#trains an svm classifier for the given training set and training labels
	def __init__(self,trainingSet,trainingLabels):
		self.trainingSet=trainingSet
		self.trainingLabels=trainingLabels
		prob = svm_problem( trainingLabels,trainingSet)
		
		#actual classifier
		self.predictor=svm_train(prob, '-t 0 -c 1')

	#instance is an array [dimension1, dimension2..]
	#predicts the label for an instance
	def predict(self,instance):
		predicted_labels, _, _= svm_predict([1],[instance],self.predictor)
		return predicted_labels



#just for testing
if __name__=="__main__":
	trainingSet=[[0,1,2], [0,1,0], [0,10,2] ]
	labels=[ 1,0,1]
	predictor1=wordPredictor(trainingSet,labels)
	print predictor1.predict([1,2,0])
