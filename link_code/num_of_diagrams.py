from libpl.pdcode import PlanarDiagram

'''
    Determines the number of diagrams in a file
'''

def num_of_diagrams(filename):
    count = 0
    z = open(filename)
    print "Counting..."
    while 1:
        try:
            a = PlanarDiagram.read(z)
            count += 1
        except:
            break
        if count % 10000 == 0:
            print "Passed ", count, " diagrams."
    z.close()
    return count
