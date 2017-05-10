# coded by Alex :D

import os.path
from libpl.pdcode import PlanarDiagram
import copy

def file_to_dict(filename):
    '''
        Standard reading of a file and returning a 
    dictionary object.
    '''

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

def master_index(homfly_index, homfly, master = "master_link_index.txt"):
    '''
        function creates and appends to a master list of all homflies found

        int homfly_index = the current found homfly number to 
            increment from

        str homfly = homfly polynomial string

        str master = master file for all homflies
    '''
    path = "/home/hollis/dev/KnotModels/link_code/test2"
    inpf = open(path + "/" + master, 'a')
    while len(homfly_index) < 10:
        homfly_index = "0" + homfly_index
    inpf.write(homfly_index + " : " + homfly + "\n")
    inpf.close()


def homfly_results(homfly_index, knot):
    '''
        function creates homfly result files       

        str homfly_index = starting homfly number
        knot = pd object of  knot 
    '''
    path = "/home/hollis/dev/KnotModels/link_code/test2/homfly_storage/"
    while len(homfly_index) < 10:
        homfly_index = "0" + homfly_index
    inpf = open(path + "/homfly_" + homfly_index + ".pdstor", 'a')
    knot.write(inpf)
    inpf.close()
    

def run_homfly(link_set):
    '''
    runs homefly for each .pdstor 

    determines whether a harddrive is plugged in
    question = input("Is your external hard drive connected? (yes/no) ")
    if question == "yes":
        pass
    else:
        raise Exception("You need a hard drive for this computation!")

    '''
    if os.path.isfile("/home/hollis/dev/KnotModels/link_code/test2/master_link_index.txt"): 
        H = file_to_dict("/home/hollis/dev/KnotModels/link_code/test2/master_link_index.txt")
    else:
        H = {}
    #if os.path.isfile("/media/alexander/HollisExt30/master_link_index.txt"): 
    z = open(link_set)
    count = 0
    while True:
        if len(H.keys()) == 0:
            mx = 0
        if len(H.keys()) != 0:
            mx = int(max(H.keys()))
        
        count += 1
        if count %10000 == 0:
            print(count)
        try:

            shadows = []
            shad = PlanarDiagram.read(z)
            num_cross = shad.ncross
            nums = 2**num_cross

            typ = "{0:0" + str(num_cross) + "b}"
            cross_types = []
            for b in range(nums):
                cross_types.append(typ.format(b))
            
            for c in range(len(cross_types)):
                knot = copy.copy(shad)
                for d in range(num_cross):
                    knot.crossings[d].sign = int(cross_types[c][d])
                shadows.append(knot)

            for iter1 in range(len(shadows)):
                new_knot = shadows[iter1]
                
                homfly = str(new_knot.homfly())
                if homfly in H.values():
                    homfly_results(str(H.values().index(homfly)), new_knot)
                else:
                    mx += 1
                    H[mx] = homfly
                    master_index(str(H.values().index(homfly)), homfly)
                    homfly_results(str(H.values().index(homfly)), new_knot)
        except:
            z.close()
            break 

## Code to run if desired

#run_homfly("/home/hollis/dev/KnotModels/link_code/test2/7.pdstor")
#pathway = "/Volumes/FantomHD/"
#for thing in range(2,11):
#    run_homfly("/Volumes/FantomHD/link_data/" + str(thing) + "/" + str(thing) + ".pdcode")
