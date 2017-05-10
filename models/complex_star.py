# Trying to make the current star diagram expandable to where we can change variables and such.
from math import pi as pi, cos as cos, sin as sin
import numpy
from libpl.pdcode import PlanarDiagram, pd_debug_off 
from libpl.pdcode import Crossing, Edge
def complex_star(number_of_sticks,*args):
    
    # First I want to create the equations of each line of the shadows.
    sticks = {} # Creating a dictionary to keep track of which stick goes with which equation.
    k = number_of_sticks
    n = (k-1)/2
    permutation_1 = []
    permutation_2 = []
    mapping = []
    if 'args' in locals():
        for ar in range(len(args)):
            if type(args[ar]) == list and permutation_1 == [] and len(args[ar]) == k:
                permutation_1 = args[ar]
            elif type(args[ar]) == list and permutation_1 != [] and len(args[ar]) == k:
                permutation_2 = args[ar]
            elif type(args[ar]) == list:
                print "Incorrect Permutations"
            else:
                mapping = int(args[ar])
    if mapping == []:
        mapping = n
    else:
        mapping = int(mapping)
    if permutation_1 == []:
        permutation_1 = numpy.random.permutation(k)
    if permutation_2 == []:
        permutation_2 = numpy.random.permutation(k)
    delt_ang = (2*pi)/k
    # Creates the change in angle to find the points.
    x_1 = {}
    x_2 = {}
    y_1 = {}
    y_2 = {}
    z_1 = {}
    z_2 = {}
    m = {}
    delt_x = {}
    delt_y = {}
    delt_z = {}
    circ_points = {}
    for p in range(k):
        x_1[p] = 10000*cos(((mapping*p)%k)*delt_ang)
        x_2[p] = 10000*cos(((mapping*p+mapping)%k)*delt_ang)
        y_1[p] = 10000*sin(((mapping*p)%k)*delt_ang)
        y_2[p] = 10000*sin(((mapping*p+mapping)%k)*delt_ang)
        z_1[p] = permutation_1[p]
        z_2[p] = permutation_2[p]
        delt_x[p] = x_2[p]-x_1[p]
        delt_y[p] = y_2[p] - y_1[p]
        delt_z[p] = z_2[p] - z_1[p]
        m[p] = (y_2[p]-y_1[p])/(x_2[p]-x_1[p])
        circ_points[p] = [10000*cos(p*delt_ang),100000*sin(p*delt_ang)]
    def find_int_xy(a,b,m,x_1,y_1,circ_points,k): #To find the intersection between two sticks a and b *add in stick numbering errors and gives the 
        if m[a] ==m[b]:
            print 'AHHH', a, b
        x = (m[a]*x_1[a] - m[b]*x_1[b] + y_1[b] - y_1[a])/(m[a]-m[b])
        y = m[a]*(x - x_1[a]) + y_1[a]
        point = [x,y]
        return point
    stick_pairs_heights = {}
    vertex_positions = {}
    t_value_y = {}
    heights_for_inter = {}
    t_values = {}
    stick_ints = {}
    for pair in range(k):
        for pair2 in range(k-3): #this would be a nice place to order the intersections in the correct order... 
            #The mapping MUST come into play here as well, solution is to find the intersection of EACH combination. 
            vertex_positions[str(pair)+','+str((pair + pair2 + 2)%k)] = find_int_xy(pair,(pair + pair2 + 2)%k,m,x_1,y_1,circ_points,k) #the order        t_value_x[str(pair)+','+str((pair + pair2 + 2)%k)] = (vertex_positions[str(pair)+','+str((pair + pair2 + 2)%k)][0]-x_1[pair])/(x_2[pair]-x_1[pair])
            t_value_y[str(pair)+','+str((pair + pair2 + 2)%k)] = (vertex_positions[str(pair)+','+str((pair + pair2 + 2)%k)][1]-y_1[pair])/(y_2[pair]-y_1[pair])
            t_value_x = t_value_y
            # Note: the t value for each stick "Should" be consistent regardless of x,y, or z..
        t_values[pair] = []
        for pair2 in range(k-3):
            t_values[pair].append((t_value_x[str(pair)+','+str((pair + pair2 + 2)%k)],(pair + pair2 + 2)%k))
            stick_pairs_heights[str(pair)+','+str((pair + pair2 + 2)%k)] = (z_1[pair] +t_value_x[str(pair)+','+str((pair + pair2 + 2)%k)]*(delt_z[pair]),z_1[(pair + pair2 + 2)%k] +t_value_x[str(pair)+','+str((pair + pair2 + 2)%k)]*(delt_z[(pair + pair2 + 2)%k]))
        t_values[pair].sort()
        stick_ints[pair] = []
        for stick in range(len(t_values[pair])):
            stick_ints[pair].append(t_values[pair][stick][1])
    #Now to create the edge information for each stick..
    edges_per_stick = []
    ne = k*k - 3*k
    for stick in range(k):
        temp = []
        for edge in range(k-2):
            temp.append((stick*(k-3)+edge)%ne)
        edges_per_stick.append(temp)
    #Now that we have all of the information needed let's create the vertices!
    vertices = []
    count = 0
    for stick in range(k):
        for position in range(k-3):
            if ((stick_ints[stick][position]%2 == 0 and stick%2 ==0) or (stick%2 == 1 and stick_ints[stick][position]%2 == 1)):
                x = 1
                y = 0
                if stick_pairs_heights[str(stick)+','+str(stick_ints[stick][position])][0] < stick_pairs_heights[str(stick)+','+str(stick_ints[stick][position])][1]:
                    v = 1
                if stick_pairs_heights[str(stick)+','+str(stick_ints[stick][position])][0] > stick_pairs_heights[str(stick)+','+str(stick_ints[stick][position])][1]:
                    v = 0
            if (stick_ints[stick][position]%2 == 0 and stick%2 ==1) or (stick%2 == 0 and stick_ints[stick][position]%2 == 1):
                x = 0
                y = 1
                if stick_pairs_heights[str(stick)+','+str(stick_ints[stick][position])][0] < stick_pairs_heights[str(stick)+','+str(stick_ints[stick][position])][1]:
                    v = 0
                if stick_pairs_heights[str(stick)+','+str(stick_ints[stick][position])][0] > stick_pairs_heights[str(stick)+','+str(stick_ints[stick][position])][1]:
                    v = 1
            vertices.append([edges_per_stick[stick][position],edges_per_stick[t_values[stick][position][1]][stick_ints[t_values[stick][position][1]].index(stick)+x],edges_per_stick[stick][position+1],edges_per_stick[t_values[stick][position][1]][stick_ints[t_values[stick][position][1]].index(stick)+y],v])
    final_verts= []
    for cutting in range((k*(k-3))/2):
        final_verts.append(vertices[cutting])
    while final_verts[(k*(k-3))/2-1][0] != 0:
        final_verts[(k*(k-3))/2-1] = [final_verts[(k*(k-3))/2-1][1],final_verts[(k*(k-3))/2-1][2],final_verts[(k*(k-3))/2-1][3],final_verts[(k*(k-3))/2-1][0],final_verts[(k*(k-3))/2-1][4]]
    final_verts.insert(0,final_verts[(k*(k-3))/2-1])
    final_verts.pop( (k*(k-3))/2)
    knot = PlanarDiagram.from_pdcode(final_verts)
    return knot
