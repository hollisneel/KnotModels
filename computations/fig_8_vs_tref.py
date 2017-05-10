from math import pi as pi, cos as cos, sin as sin
import numpy
from libpl.pdcode import PlanarDiagram, pd_debug_off 
from libpl.pdcode import Crossing, Edge
#Goal for this program is to check the ratio of the trefoil vs. the figure-eight knot. For arbritrairily stick size.. I want to run both types of models to see if they approach 28%! Let's find out
import itertools

#Ok so we now have both models in this program.. odd_point_star() is the analog for the Petalua model, complex_star for my modified version..
def fig_8_vs_tref(odd_number_of_sticks, number_of_knots):
    ''' runs number_of_knots (integer) odd_point_star(number_of_sticks) and compares the number of figure eight knots versus trefoil knots '''
    k = odd_number_of_sticks
    if k%2 == 0:
        return 
    n = k-1/2
    if n == 4 or n == 5:
        permutation = list(itertools.permutations(range(2*n-1),(2*n-1)))
        if n > 5:
            permutation = []
            for p in range(1000):
                permutation.append(numpy.random.permutation(2*n-1))
                tref = 0
                figeight = 0
                count = 0
                for r in range(len(permutation)):
                    print count
                    count += 1
                    a = KnotModels.odd_point_star((k),permutation[r])
                    if str(a.homfly()) == '-2a^{2} + a^{2}z^{2} + -a^{4}':
                        tref += 1
                    if str(a.homfly()) == '-a^{-2} + -1 + z^{2} + -a^{2}':
                        figeight += 1
    return figeight/tref
