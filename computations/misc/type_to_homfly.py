from libpl.pdcode import PlanarDiagram

'''
    type_to_Homfly.py

    Written by: Nicholas Neel

    purpose : To obtain the homfly 
'''
def type_to_homfly(string,edges):

	# Obtain all knot info
	compsPos = [-1]
	for a in range(len(string)):
		if string[a] == "#":
			compsPos.append(a)
	compsPos.append(len(string))
	knot_type = []


	for a in range(len(compsPos)-1):
		knot_type.append(string[compsPos[a]+1:compsPos[a+1]].replace(" ",""))

	# find knot table line 
	z = open(PlanarDiagram.KNOT_NAMES,'r')
	namedataRAW = z.readlines()
	z.close()
	index = []
	for a in range(len(namedataRAW)):
		for c in knot_type:
			namedataRAW[a] = namedataRAW[a].replace(" ","")
			if namedataRAW[a][0: len(c)].replace(" ","") == c:
				index.append(a)

	z = open(PlanarDiagram.KNOT_TABLE,'r')
	tempData = z.readlines()
	z.close()
	tempdatatostr = ""
	for a in tempData:
		tempdatatostr += a
	tempData = tempdatatostr.split("\n")
	knotsList = []

	for a in index:
		knotsList.append(tempData[a])

	return knotsList
