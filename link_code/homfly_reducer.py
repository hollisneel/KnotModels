# code that will reduce homflies (hopefully) into splittable and not splittable

import os
import glob
from libpl.pdcode import PlanarDiagram

#path = "/media/alexander/HollisExt30/"
#new_path = path + "reduced_homfly_storage/"

#path = "/home/hollis/dev/KnotModels/link_code/test/"
path = "/Users/Alex/Research/Mathematics/KnotModels/link_code/test/"

def link_reduce(homfly):
    z = open(path + "homfly_storage/" + homfly)
    split_file = open(path +"reduced_homfly_storage"+"/splittable_" + homfly, 'a')
    unsplit_file = open(path + "reduced_homfly_storage"+"/unsplittable_" + homfly, 'a')
    count = 0
    knots = []
    while True:
        count += 1
        if count %10000 == 0:
            print(count)
        try:
            knot = PlanarDiagram.read(z)
            linking_num = []
            is_written = 0

            for comp1 in range(knot.ncomps):
                for comp2 in range(knot.ncomps):
                    ln = knot.linking_number(comp1,comp2)
                    if comp1 != comp2:
                	    linking_num.append(ln)
            if linking_num.count(0) == 0:
                num_isotopies = 0

                if len(knots)==0:
                    knots.append(knot)
                    continue
                for a in knots:
                    if a.isotopic(knot):
                        num_isotopies += 1
                        break

                if num_isotopies == 0:
                    knots.append(knot)
#                    knots.write(unsplit_file)
                    is_written = 1

            if linking_num.count(0) != 0:
                if len(knot.simplify()) == 1:
                    num_isotopies = 0

                    if len(knots) == 0:
                        knots.append(knot)
                        continue

                    for a in knots:
                        if a.isotopic(knot):
                            num_isotopies += 1
                            break

                    if num_isotopies == 0:
                        knots.append(knot)
#                        knots.write(unsplit_file)
                        is_written = 1

            if (not is_written):
                knot.write(split_file)


        except:
            break
    knots.write(unsplit_file)
#    print "Number of knots :", len(knots)
#    reduced = isotopic_reduce2(knots)
    split_file.close()
    unsplit_file.close()

for f in os.listdir(path + "homfly_storage/"):
    print(f)
    link_reduce(f)
