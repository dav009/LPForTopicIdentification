class frecuencyTable:

	def __init__(self);
		#just init the dictionary holding the data
		table={}


	#adds a new record to the table
	#updates the frecuency of that record if it already exists
	def add(self,key):
		if(key in table):
			table[key]=table[key]+1
		else:
			table[key]=1



	def sort_by_value(self):
	    #returns the items of the dictonary sorted by theirvaue
	    items=table.items()
	    backitems=[ [v[1],v[0]] for v in items]
	    backitems.sort()
	    return [ backitems[i][1] for i in range(0,len(backitems))]
