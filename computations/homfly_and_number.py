from math import pi as pi, cos as cos, sin as sin
import numpy
from libpl.pdcode import PlanarDiagram, pd_debug_off 
from libpl.pdcode import Crossing, Edge
import itertools
import KnotModels

def homfly_and_number(number_of_chords):
    '''Creates a file which creates a document with all computed HOMFLY polynomials and how many times they appear in the number_of_chords star diagram model. Creates documents in current directory. '''
    k = number_of_chords
    n = (k-1)/2
    z = open('HOMFLY' + str(k) + '.txt','w')
    HOMFLY = []
    count = 0
    if n == 3 or n == 4 or n == 5:
        permutation = list(itertools.permutations(range(2*n-1),(2*n-1)))
    if n > 5:
        permutation = []
        for p in range(1000000):
            permutation.append(numpy.random.permutation(2*n-1))
    for r in range(len(permutation)):
        print count , ' : ', str(len(permutation)-1)
        count += 1
        a = odd_point_star((2*n-1),permutation[r])
        HOMFLY.append(str(a.homfly()))
    HOM_DICT = {}
    count2 = 0
    for HOM in range(len(HOMFLY)):
        print count2, ' : ', str(len(HOMFLY)) 
        count2 += 1
        HOM_DICT[HOMFLY[HOM]] = HOMFLY.count(HOMFLY[HOM]) 
    z.write(str(HOM_DICT))
    z.close()
