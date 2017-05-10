import odd_point_star, itertools, numpy, math, sys, select, os

'''
    compute_homflies.py

    Written by: Nicholas Neel

'''

# Creates a file using n sample files
def compute(p,n=-1,name = ""):
    '''
        compute(p,n,name)
    
        int p = number of points on a star
        int n = number of desired iterations
                (set to all by default)

        str name = the path to output file
                (set to p_star_Homflies.txt by default)

        Purpose : To compute the homflies of a large(if not all)
        samples of star knots.

    '''
    # Open a file to record results
	if name == "":
		z = open(str(p) + "_star_Homflies.txt",'a')	
	else :
		z = open(name,'a')

    # create variables to store data.
	permutations = []
	cleanHomflyDict = {}

    # While loop counter and number of iterations creator
	count = 1
	if n == math.factorial(p) or n == -1:
		permutations = list(itertools.permutations(range(p)))
	else:
		for a in range(n):
			permutations.append(numpy.random.permutation(p))


    # Run through iterations and add similar homflies
	x = 0
	while x < len(permutations):
		
		PDobject = odd_point_star.odd_point_star(p,permutations[x])
		PDhomfly = PDobject.homfly()
		
		if cleanHomflyDict.has_key(PDhomfly):
			cleanHomflyDict[PDhomfly] = cleanHomflyDict[PDhomfly] + 1
		
		else :
			cleanHomflyDict[PDhomfly] = 1
		if count%1000 == 0:
		    print str(p) + " : " + str(count) + " / " + str(len(permutations))
		count += 1
		x += 1	

    # Write homflies to file
	for y in range(len(cleanHomflyDict.keys())):
		z.write(str(cleanHomflyDict.keys()[y]) + " : " + str(cleanHomflyDict[cleanHomflyDict.keys()[y]]) + ",\n")
	z.close()
	return


def printDictToFile(filename,dictionary):
    '''
        printDictToFile(filename,dictionary)
    
        str  filename   = name/path of file to write to
        dict dictionary = dictionary object to write to file

        Purpose : 
            To expand the potential saving dictionaries whose 
        size may increase the current computers ram
    '''

	z = open(filename, 'w')
	for y in range(len(dictionary.keys())):
		z.write(str(dictionary.keys()[y]) + " : " + str(dictionary[dictionary.keys()[y]]) + ",\n")
	z.close()



def readInDict(name):
    '''
        readInDict(name)

        str name = path/name of file to read

        Purpose : 
            To expand the potential saving dictionaries whose 
        size may increase the current computers ram
    '''

	fileobj = open(name,'r')
	raw_str = str(fileobj.readlines())
	raw_str = raw_str.replace(',\\n', "")
	raw_str = raw_str.replace("'","")
	raw_str = raw_str.replace("[","")
	raw_str = raw_str.replace("]","")
	places = [-1]
	keysvals = []
	result = {}
	oddlst = []
	badportion = []
	for a in range(len(raw_str)):
		if raw_str[a] == ',' or raw_str[a] == ':':
			places.append(a)
	places.append(len(raw_str))
	a = 0
	while a+2 < len(places):
		if raw_str[places[a+1]+1:places[a+2]].strip().isdigit():
			keysvals.append([raw_str[places[a]+1:places[a+1]].strip(),int(raw_str[places[a+1]+1:places[a+2]].strip())])
		else :
			a += 1
			if raw_str[places[a+1]+1:places[a+2]].strip().isdigit():
				oddlst.append([raw_str[places[a]+1:places[a+1]].strip(),int(raw_str[places[a+1]+1:places[a+2]].strip())])
		a += 2
	for it in range(len(keysvals)):
		if result.has_key(keysvals[it][0]):
			result[keysvals[it][0]] += keysvals[it][1]
		else :
			result[keysvals[it][0]] = keysvals[it][1]
	fileobj.close()
	if len(oddlst) > 0:
		print "errors in file!"
		print "Suggest cleanfile(file)"
	return result

def numOfPts(dictionary):
    '''
        numOfPts(dictionary)

        dict dictionary = dictionary to count points

        Purpose :
            To error check the number of computed points
    '''

	keys = dictionary.keys()
	summ = 0
	for a in range(len(keys)):
		summ += dictionary[keys[a]]
	return summ

def cleanfile(name):
    '''
        cleanfile(name)
    
        str name = name/path of potentially currupt file

        purpose:
            To clean a file in the case of improper file usage.
    '''
	A = readInDict(name)
	printDictToFile("reduced" + name,A)

def justStars(p,n):
    '''
        justStars(p,n,name)

        int p = number of points in star knot
        int n = number of desired points.
        str name = name/path of output file

        Purpose:
            creates a list of PDobjects to be used however
        the user desires.

    '''

	permutations = []
	diags = []
	if n == math.factorial(p) or n == 'a':
	        permutations = list(itertools.permutations(range(p)))
	else :
		for a in range(n):
			permutations.append(numpy.random.permutation(p))

	for a in range(len(permutations)):
		diags.append(odd_point_star.odd_point_star(p,permutations[a]))
		if a%1000 == 0 :
			print str(a) +" / " + str(len(permutations))
	return diags

