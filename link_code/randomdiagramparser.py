import os.path, os
from libpl.pdcode import PlanarDiagram

def random_diagram_parser(string):
    name = "/home/hollis/dev/randomdiagram/src/" + string
    pdcode = open(name)
    pdcode.readline()

    dest = open("/home/hollis/dev/KnotModels/link_code/shadows/"+string[0:1]+".pdstor", "a" )	
    count = 1
    while 1:
        try:
            diag = PlanarDiagram.read(pdcode)
            if diag.ncomps > 1:
                diag.write(dest)
        except:
            count += 1
            if count > 10:
               break        
        
    pdcode.close()
    dest.close()
	
    print "Finished : "
