from libpl.pdcode import PlanarDiagram
import plink, os

'''
    Draw a knot and save it to a pdstor file format
'''

def plink_write():
    z = ()
    c = raw_input("save file as: ")
    a = plink.LinkEditor()
    z = raw_input("Press Enter When Finished With Plink")
    a.zoom_to_fit()
    #a.save_as_eps('~/Desktop/Knot_Table/' +str(c) + '.eps' , 'gray') #saves picture
    b = PlanarDiagram.from_plink(a)
    e = open(str(c) + '.pdstor','w' )
    b.write(e)
    e.close()
    a.done

