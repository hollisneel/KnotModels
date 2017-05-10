from libpl.pdcode import PlanarDiagram

def pd_isotopy(knot):
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


def is_isotopic(knot1,knot2):
    self = knot1
    knot = knot2
    ncomps = knot.ncomps
    nedges = knot.nedges
    if self.ncross != knot.ncross or self.nedges != knot.nedges or self.ncomps != knot.ncomps:
        return False

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
            for pos in len(orient):
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


