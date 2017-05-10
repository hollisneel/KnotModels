import os, snappy
from libpl.pdcode import PlanarDiagram

 
def as_snappy_manifold(knot): 
    try:
        knot1 = knot.snappy_manifold()
        return knot1
    except:
        return -1

def hyperbolic_volume_reduce(pd_list):
    
    #First we need to convert from plcurve to snappy
    volumes = {"0":[]}
    snp_list = []
    for a in pd_list:
        val = as_snappy_manifold(a)
        if type(val) == int:
            volumes["0"].append(a) 
        if type(as_snappy_manifold(a)) != int:
            snp_list.append(as_snappy_manifold(a)) 
    # Next, we need to create a dictionary of the volume as the key
    # and the knots with those values as the key.
    # In original pd format.

    for a in range(len(snp_list)):
        vol = str(snp_list[a].volume())
        if volumes.has_key(vol):
            volumes[vol].append(pd_list[a])
        if not volumes.has_key(vol):
            volumes[vol] = [pd_list[a]]

    return volumes


def max_cusp_volume_reduce(pd_list):
    
    #First we need to convert from plcurve to snappy
    volumes = {"0":[]}
    snp_list = []
    for a in pd_list:
        val = as_snappy_manifold(a)
        if type(val) == int:
            volumes["0"].append(a)
        if type(val) != int:
            snp_list.append(as_snappy_manifold(a))
  
    # Next, we need to create a dictionary of the volume as the key
    # and the knots with those values as the key.
    # In original pd format.
    
    for a in len(snp_list):
        man = snp_list[a].cusp_neighborhood()
        vol = str(snp_list[a].volume())
        
        # It needs to be verified that a manifold's
        # cusp_neighborhood's volume is in fact the maximal
        # cusp volume!!


        if volumes.has_key(vol):
            volumes[vol].append(pd_list[a])
        if not volumes.has_key(vol):
            volumes[vol] = [pd_list[a]]   
    return volumes  


def easy_splittable(pd_list):
    res = {"splittable":[],"unsplittable":[]}

    for a in pd_list:
        val = a.simplify()
        if len(val) >1:
            res["splittable"].append(a)
        if len(val) == 1: 
            val = val[0]
            val.regenerate()
            res["unsplittable"].append(val)
    return res


def linking_number_reduce(pd_list):
    link_res = {}
    
    for a in pd_list:
        temp_list = []

        for val1 in range(int(a.ncomps)):
            for val2 in range(int(a.ncomps)):
                if val1 != val2 and val1 < val2:
                    temp_list.append(a.linking_number(val1,val2))

        temp_list.sort()
        if link_res.has_key(str(temp_list)):
            link_res[str(temp_list)].append(a)
        if not link_res.has_key(str(temp_list)):
            link_res[str(temp_list)] = [a]

    return link_res



def isotopic_reduce(pdlist):
    #Always run AFTER easy_splittable

    isotopic_res = {"isotopic_unique":[],"isotopic_to_unique":[]}
    ##############
    #count = 0
    #lst = list(pdlist)
    #for a in range(len(lst)):
    #    for b in range(len(lst)):
    #        try:
    #            if a != b and is_isotopic(lst[a],lst[b]):
    #                isotopic_res["isotopic_to_unique"].append(lst[b])
    #                lst.pop(b)
    #        except:
    #            count += 1
    #            if a == len(pdlist):
    #                break
    #isotopic_res["isotopic_unique"] = lst
    #############
    for a in range(len(pdlist)):       
        if len(isotopic_res["isotopic_unique"]) == 0:
            isotopic_res["isotopic_unique"].append(pdlist[a])
            continue
        for b in range(len(isotopic_res["isotopic_unique"])):
            knot2 = isotopic_res["isotopic_unique"][b]
            if pdlist[a].isotopic(knot2):
                isotopic_res["isotopic_to_unique"].append(pdlist[a])
                break
            if b == len(isotopic_res["isotopic_unique"])-1:
                isotopic_res['isotopic_unique'].append(pdlist[a])
    ############
    #sieve = list(pdlist)
    #unique = []
    #non = []
    #for a in range(len(sieve)):
    #    if type(sieve[a]) == int:
    #        continue
    #    knot1 = pdlist[a]
    #    sieve[a] = 0
    #    unique.append(knot1)
    #    for b in range(len(sieve)):
    #        if a < b and type(sieve[b]) != int and is_isotopic(knot1,sieve[b]):
    #            non.append(sieve[b])
    #            sieve[b] = 0
    #    print len(unique)
    ###########
    #return {"isotopic_unique":unique,"isotopic_to_unique":non}
    return isotopic_res    
        
       #filling in zeros when they are isomorphic  
         
def isomorphic_reduce(pdlist):
    isomorphic_res = {"isomorphic_unique":[],"isomorphic_to_unique":[]}
    for a in range(len(pdlist)):
        if len(pdlist[a].simplify()) != 1:
            print "warning splittable component will/HAS lost data"
            newpdlist = easy_splittable(pdlist)
            pdlist = newpdlist["unsplittable"]
            return isomorphic_reduce(pdlist)
        if len(isomorphic_res["isomorphic_unique"]) == 0:
            isomorphic_res["isomorphic_unique"].append(pdlist[a])
            continue
        for b in range(len(isomorphic_res["isomorphic_unique"])):
            knot2 = isomorphic_res["isomorphic_unique"][b]
            if pdlist[a].isomorphic(knot2):
                isomorphic_res["isomorphic_to_unique"].append(pdlist[a]    )
                break
 
            if b == len(isomorphic_res["isomorphic_unique"])-1:
                isomorphic_res['isomorphic_unique'].append(pdlist[a])
    return isomorphic_res

############################
#
# pdisotopy code below   
#
############################


def pd_isotopy(knot):
    '''
    Takes a knot and returns a knot isotopy by shifting all edges +1
    '''
    cross_info = []
    ne = knot.nedges
    for a in knot.crossings:
        temp = [-1,-1,-1,-1,-1]
        for b in range(2):
            temp[a.overstrand_pos()[b]] = a.overstrand_indices()[b]
        for b in range(2):
            temp[a.understrand_pos()[b]] = a .understrand_indices()[b]
        temp[4] = a.sign
        cross_info.append(temp)
    verts = []
    for a in cross_info:
        new_vert = []
        for b in range(4):
            old_val = a[b]
            new_vert.append((old_val +1)%ne)

        while new_vert[0] > new_vert[1] or new_vert[0] > new_vert[2] or new_vert[0] > new_vert[3]:
            new_vert = [new_vert[1],new_vert[2],new_vert[3],new_vert[0]] 

        new_vert.append(a[4])
        verts.append(new_vert)
    verts.sort()
    knot2 = PlanarDiagram.from_pdcode(verts)
    for a in range(len(verts)):
        knot2.crossings[a].sign = verts[a][4]
    return knot2


#####################


def is_isotopic(knot1,knot2):
    self = knot1
    knot = knot2
    ncomps = knot.ncomps
    nedges = knot.nedges
    if self.ncross != knot.ncross or self.nedges != knot.nedges or self.ncomps != knot.ncomps:
        return False
    if knot1.isotopic(knot2):
        return True
    changes = []
    tempknot = knot

    for a in range(nedges/ncomps):
        new_knot = pd_isotopy(tempknot)
        if self.isotopic(new_knot):
            return True

        tempknot = new_knot

    if knot1.homfly() == knot2.homfly():
        typ = "{0:0"+str(ncomps)+"b}"
        for b in range(ncomps*ncomps):
            changes.append(typ.format(b))
        
        for orient in changes:
            for pos in range(len(orient)):
                if pos == "0":
                    self = self
                if pos == "1":
                    knot.reorient_component(pos,1)

            tempknot = knot

            for a in range(nedges):
                newknot = pd_isotopy(tempknot)
                if self.isotopic(newknot):
                    return true

    if knot1.homfly() != knot2.homfly():
        return False

    return False
