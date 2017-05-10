from libpl.pdcode import PlanarDiagram
import os


#######################################
def isometry_reduce(file_path):
    z = open(file_path)
    pdcodes = []
    while 1:
        try:
            pdcodes.append(PlanarDiagram.read(z))
        except:
            break
    z.close()
    # Now I have all pd in ram

    splittable = []
    non_split = []
    isom_un = []
    non_un = []
    print len(pdcodes)
    for a in pdcodes:
        pot = a.simplify()
        if len(pot) != 1:
            splittable.append(a)
        if len(pot) == 1:
            knot = pot[0]
            knot.regenerate()
            non_split.append(knot)
    
    pdlist = list(non_split) 
    if len(non_split) != 0:
        isom_un.append(pdlist[0])
        pdlist[0] = 0
    for a in range(len(pdlist)):
        for b in range(len(isom_un)):
            if type(pdlist[a]) != int and pdlist[a].isomorphic(isom_un[b]) :
                non_un.append(pdlist[a])
                pdlist[a] = 0
            if type(pdlist[a])!= int and b == len(isom_un)-1:
                isom_un.append(pdlist[a])
                pdlist[a] = 0
    
    f1 = open(file_path[0:len(file_path)-7] + "_unique.pdstor","a")
    f2 = open(file_path[0:len(file_path)-24]+"non_unique/"+file_path[len(file_path)-24:len(file_path)-7] + "_isom.pdstor","a" ) 
    splitfile = open(file_path[0:len(file_path)-24]+"non_unique/"+file_path[len(file_path)-24:len(file_path)-7] + "_splittable.pdstor" ,"a")
    os.remove(file_path)
    for a in isom_un:
        a.write(f1)
    for a in non_un:
        a.write(f2)
    for a in splittable:
        a.write(splitfile)
    f1.close()
    f2.close()
    splitfile.close()
    return        
def isom_reduce_folder(folder_path):

    dirs = list(os.listdir(folder_path))
    os.mkdir(folder_path + "non_unique")
    for a in dirs:
        isometry_reduce(folder_path + a)
    return
#######################################

#######################################
def vred(file_path):
    z = open(file_path)
    pdcodes = []
    while 1:
        try:
            pdcodes.append(PlanarDiagram.read(z))
        except:
            break
    human_reduced = []
    pl0 = pdcodes[0].as_spherogram().view()
    keep = [pdcodes.pop(0)]

    for a in range(len(pdcodes)):
        if type(pdcodes[a]) == int:
            continue
        pl = pdcodes[a].as_spherogram().view()
        delete = raw_input("isotopic? y/n : ")
        pl.done()
        if delete == 'y':
            human_reduced.append(pdcodes[a])
        if delete == 'n':
            keep.append(pdcodes[a])
    pl0.done()
    f1 = open(file_path[0:len(file_path)-31] + "human_reduced/"+file_path[len(file_path)-31:len(file_path)],"a") 
    f2 = open(file_path[0:len(file_path)-14] + ".pdstor","a")
    for a in human_reduced:
        a.write(f1)
    for a in keep:
        a.write(f2)
    os.remove(file_path)
    f1.close()
    z.close()
    f2.close()


def view_reduce(folder_path):
    dirs = list(os.listdir(folder_path))
    if not os.path.isdir(folder_path+ "human_reduced"):
        os.mkdir(folder_path+"human_reduced")
    for a in dirs:
        vred(folder_path + a)
    return
#######################################

#######################################
def clean_folder(folder_path):

    directories = list(os.listdir(folder_path))
    for a in directories:
        if os.path.isfile(folder_path + a):
            run_simplify(folder_path + a,len(a))
    return

def run_simplify(file_path,length):
    pdcodes = []
    z = open(file_path)
    while 1:
        try:
            pdcodes.append(PlanarDiagram.read(z))
        except:
            break
    z.close()
    if len(pdcodes) == 1 and length != 24:
        
        f1 = open(file_path[0:len(file_path)-14]+".pdstor","a")
        pdcodes[0].write(f1)
        f1.close()
        os.remove(file_path)
    if len(pdcodes) == 0 :
        os.remove(file_path)
    
    return
#######################################
