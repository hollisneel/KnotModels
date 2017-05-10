from libpl.pdcode import PlanarDiagram
import os

''' 
    Removes currupted pdcode
'''
    
def pdcode_fix(filename):
    z = open(filename)
    z2 = open(filename + "f","a")
    count = 0
    while 1:
        while 1:
            try:
                PlanarDiagram.read(z).write(z2)
                count += 1
            except:
                break
            if count%10000 == 0:
                print count
        try:
            PlanarDiagram.read(z).write(z2)
            count += 1
        except:
            break
    z.close()
    z2.close()
