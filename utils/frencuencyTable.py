#author: David Przybilla
#date: July 2012
#this class is a frequencyTable for counting how many times a word appears in a text
class frecuencyTable:

	def __init__(self):
		#just init the dictionary holding the data
		self.table={}


	#adds a new record to the table
	#updates the frecuency of that record if it already exists
	def add(self,key):
		if(key in self.table):
			self.table[key]=self.table[key]+1
		else:
			self.table[key]=1

	def get(self,key):
		if(key in self.table):
			return self.table[key]
		else:
			return 0


	def getKeys(self):
		return self.table.keys()



	def sort_by_value(self):
	    #returns the items of the dictonary sorted by theirvaue
	    items=self.table.items()
	    backitems=[ [v[1],v[0]] for v in items]
	    backitems.sort()
	    return [ backitems[i][1] for i in range(0,len(backitems))]
