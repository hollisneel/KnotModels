from libpl.pdcode import PlanarDiagram
'''
    Prints the number of planar diagrams in a file
'''

def counter(file_name):
	fil = open(file_name)
	count = 0
	while 1:
		a = PlanarDiagram.read(fil)
		count += 1
		print count
