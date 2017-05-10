# coded by Alex :D

import os.path
from libpl.pdcode import PlanarDiagram

def file_to_dict(filename):
	z = open(filename)
	Str = z.read()
	Colon_Comma = [-1]
	Dict = {}
        z.close()
	for a in range(len(Str)):
		if Str[a] == ":":
			Colon_Comma.append(a)
		if Str[a] == "\n":
			Colon_Comma.append(a)
	Colon_Comma.append(len(Str))
	a = 0
	while a+2 < len(Colon_Comma):
		if a == 0:
			Dict[Str[0:Colon_Comma[a+1]].strip()] = Str[Colon_Comma[a+1]+1:Colon_Comma[a+2]].strip()
		else:
			Dict[Str[Colon_Comma[a]:Colon_Comma[a+1]].strip()] = Str[Colon_Comma[a+1]+1:Colon_Comma[a+2]].strip()
		a += 2
	return Dict

# function creates and appends to a master list of all homflies found
def master_index(homfly_index, homfly, master = "master_link_index.txt"):
    path = "/media/alexander/HollisExt30/"
    inpf = open(path + "/" + master, 'a')
    while len(homfly_index) < 10:
        homfly_index = "0" + homfly_index
    inpf.write(homfly_index + " : " + homfly + "\n")
    inpf.close()

# function creates homfly result files
def homfly_results(homfly_index, knot):
    path = "/media/alexander/HollisExt30/homfly_storage/"
    while len(homfly_index) < 10:
        homfly_index = "0" + homfly_index
    inpf = open(path + "/homfly_" + homfly_index + ".pdstor", 'a')
    knot.write(inpf)
    inpf.close()
    
# runs homefly for each .pdstor 
def run_homfly(link_set):
    """
    # determines whether a harddrive is plugged in
    question = input("Is your external hard drive connected? (yes/no) ")
    if question == "yes":
        pass
    else:
        raise Exception("You need a hard drive for this computation!")
    """
    if os.path.isfile("/media/alexander/HollisExt30/master_link_index.txt"): 
        H = file_to_dict("/media/alexander/HollisExt30/master_link_index.txt").values()
    else:
        H = []
    #if os.path.isfile("/media/alexander/HollisExt30/master_link_index.txt"): 
    z = open(link_set)
    count = 0
    while True:
        count += 1
        if count %10000 == 0:
            print(count)
        try:
            new_knot =  PlanarDiagram.read(z)
            homfly = str(new_knot.homfly())
            if homfly in H:
                homfly_results(str(H.index(homfly)), new_knot)
            else:
                H.append(homfly)
                master_index(str(H.index(homfly)), homfly)
                homfly_results(str(H.index(homfly)), new_knot)
        except:
            break 

#run_homfly("../../link_data/data/2/2_links.pdstor")
