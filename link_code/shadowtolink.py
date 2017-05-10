from libpl.pdcode import PlanarDiagram

'''
   Converts knot shadows (frm all diagrams) to links 
'''


for a in range(10,11):
	#name =  "/media/alexander/HollisExt30/link_data/data/" + str(a) +"/" + str(a) +  ".pdcode"
	name =  "/media/hollis/HollisExtTB/link_data/data/" + str(a) +"/" + str(a) +  ".pdcode"

    j = a
	fil1 = open(name)
	
	num = 1


	all_links = []
	#fil = open("/media/alexander/HollisExt30/link_data/data/" + str(a) + "/"+ str(a)+"_links.pdstor","a")
    fil = open("/media/hollis/HollisExtTB/link_data/data/" + str(a) + "/"+ str(a)+"_links.pdstor","a")

	count = 0

	print "Starting"
	while num:
		try:
			a = PlanarDiagram.read(fil1)
			num_cross = a.ncross
			nums = 2**num_cross
			typ = "{0:0" + str(num_cross) + "b}"
			cross_types = []
			for b in range(nums):
				cross_types.append(typ.format(b))
			for c in range(len(cross_types)):
				for d in range(num_cross):
					a.crossings[d].sign = int(cross_types[c][d])
				a.write(fil)
			count += 1
			if count%1000 == 0:
				print "finished " + str(count)
		except EOFError:
			num = 0
    fil.close()
	print "finished " ,a								 
