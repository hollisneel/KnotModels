# returns a planar diagram object and a picture of the star diagram
import math, pylab, matplotlib, numpy, itertools, os, os.path, sys
from mpl_toolkits.mplot3d import proj3d
from itertools import product, compress, izip, permutations
from libpl.pdcode import PlanarDiagram, pd_debug_off 
from libpl.pdcode import Crossing, Edge
def star_knot(k, *permutation):

    if permutation == ():
        permutation = numpy.random.permutation(k)
    if permutation != ():
        permutation = permutation

    def draw_odd_point_star(k,permutation):
        points = []
        lines  = []
        for p in range(k):
	    points.append((math.cos((2*(3.14159)*p)/k),math.sin((2*(3.14159)*p)/k)))
        for j in range(len(points)):
            l = j*((k-1)/2)%k
            lines.append([points[l],points[(l+(k-1)/2)%k]])

        fig = matplotlib.pyplot.figure()
        ax  = fig.add_subplot(110, projection = '3d')
        for h in range(k):
            ax.plot([lines[h][0][0],lines[h][1][0]],[lines[h][0][1],lines[h][1][1]],permutation[h],'k',linewidth=3)
            ax.plot([lines[h][0][0],lines[h][1][0]],[lines[h][0][1],lines[h][1][1]],permutation[h],'w',linewidth=1)
            ax.plot([lines[h][0][0],lines[h][0][0]],[lines[h][0][1],lines[h][0][1]],[permutation[h],permutation[(h-1)%k]],'k',linewidth=3)
            ax.plot([lines[h][0][0],lines[h][0][0]],[lines[h][0][1],lines[h][0][1]],[permutation[h],permutation[(h-1)%k]],'w',linewidth=1)
       
            ax.scatter(lines[h][0][0],lines[h][0][1],permutation[h],c='k')
            ax.scatter(lines[h][0][0],lines[h][0][1],permutation[(h-1)%k],c='k')
#        def orthogonal_proj(zfront, zback):
#            a = (zfront+zback)/(zfront-zback)
#            b = -2*(zfront*zback)/(zfront-zback)
#            return numpy.array([[1,0,0,0],
#                        [0,1,0,0],
#                        [0,0,a,b],
#                        [0,0,0,zback]])
#        proj3d.persp_transformation = orthogonal_proj
        a = matplotlib.pyplot.get_current_fig_manager()
        z = str(raw_input('Would you like the plot in full screen? y/n  '))
        ax.view_init(90,270)
        ax.grid(False)
        matplotlib.pyplot.axis('off')
        matplotlib.pyplot.title(r'$\pi = $' + str(permutation)+',   n = ' + str((k-1)/2) + ',   k = ' + str(k))
        if z == 'y':
            a.full_screen_toggle()
            matplotlib.pyplot.title(r'$\pi = $' + str(permutation)+',   n = ' + str((k-1)/2) + ',   k = ' + str(k) + '    press ctr + f to quit')
        matplotlib.pyplot.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
        matplotlib.pyplot.show()
        return 
 

    def odd_point_star(k,permutation):
        SS = []
        p = permutation
        for e in range(k):
            for e1 in range(k):
                if (permutation[e] == permutation[e1]) and (e != e1):
                    print 'This is not a correct permutation'
                    return 'error'
        if len(p) != k:
            print 'This is not a correct permutation'
            return 'error'
        for m in range(k):
            for i in range((k-3)/2):
                SS.append((m+(k-2*i-3))%k)
            for i in range((k-3)/2):
                SS.append((m+(k-2*i-2))%k)
                Stick_crossing_order = {}
            for m in range(k):
                Stick_crossing_order[m] = SS[(((k-3)*m)):((k-3)*(m+1))]
        ES = []
        for y in range(k):
            for x in range(k-2):
                ES.append((x+(k-3)*y)%(k*(k-3)))
        edges_stick = {}
        for z in range(k):
            edges_stick[z] = ES[(z*(k-2)):(z*(k-2)+(k-2))]
       
        nv = (((k*k)-(3*k))/2)
        count = -1
        total = {}
        crossing_values = []
        for stick in range(k):
            for position in range(k-3):
                x = Stick_crossing_order[Stick_crossing_order[stick][position]].index(stick)
                if x < (k-3)/2:
                    edge_and_next = [edges_stick[Stick_crossing_order[stick][position]][x],edges_stick[Stick_crossing_order[stick][position]][x+1]]
                if x >= (k-3)/2:
                    edge_and_next = [edges_stick[Stick_crossing_order[stick][position]][x+1],edges_stick[Stick_crossing_order[stick][position]][x]]     
       
                if stick < Stick_crossing_order[stick][position]:
                    if ((stick%2) == 0) and ((Stick_crossing_order[stick][position]%2) == 0):
                        if p[stick] < p[Stick_crossing_order[stick][position]] :
                            edge_and_next.append(True)
                        if p[stick] > p[Stick_crossing_order[stick][position]] :
                            edge_and_next.append(False)
                        if p[stick] == p[Stick_crossing_order[stick][position]]:
                            edge_and_next.append('skip1')
                    if ((stick%2) == 0) and ((Stick_crossing_order[stick][position]%2) == 1):
                        if p[stick] > p[Stick_crossing_order[stick][position]] :
                            edge_and_next.append(True)
                        if p[stick] < p[Stick_crossing_order[stick][position]] :
                            edge_and_next.append(False)
                        if p[stick] == p[Stick_crossing_order[stick][position]]:
                            edge_and_next.append('skip2')
                    if ((stick%2) == 1) and ((Stick_crossing_order[stick][position]%2) == 0):
                        if p[stick] > p[Stick_crossing_order[stick][position]]:
                            edge_and_next.append(True)
                        if p[stick] < p[Stick_crossing_order[stick][position]]:
                            edge_and_next.append(False)
                        if p[stick] == p[Stick_crossing_order[stick][position]]:
                            edge_and_next.append('skip3')
                    if ((stick%2) == 1) and ((Stick_crossing_order[stick][position]%2) == 1):
                        if p[stick] < p[Stick_crossing_order[stick][position]]:
                            edge_and_next.append(True)
                        if p[stick] > p[Stick_crossing_order[stick][position]]:
                            edge_and_next.append(False)
                        if p[stick] == p[Stick_crossing_order[stick][position]]:
                            edge_and_next.append('skip4')
    
                if stick > Stick_crossing_order[stick][position] :
                    if ((stick%2) == 0) and ((Stick_crossing_order[stick][position]%2) == 0):
                        if p[stick] > p[Stick_crossing_order[stick][position]] :
                            edge_and_next.append(True)
                        if p[stick] < p[Stick_crossing_order[stick][position]] :
                            edge_and_next.append(False)
                        if p[stick] == p[Stick_crossing_order[stick][position]]:
                            edge_and_next.append('skip5')
                    if ((stick%2) == 0) and ((Stick_crossing_order[stick][position]%2) == 1):
                        if p[stick] < p[Stick_crossing_order[stick][position]] :
                            edge_and_next.append(True)
                        if p[stick] > p[Stick_crossing_order[stick][position]] :
                            edge_and_next.append(False)
                        if p[stick] == p[Stick_crossing_order[stick][position]]:
                            edge_and_next.append('skip6')
                    if ((stick%2) == 1) and ((Stick_crossing_order[stick][position]%2) == 0):
                        if p[stick] < Stick_crossing_order[stick][position]:
                            edge_and_next.append(True)
                        if p[stick] > p[Stick_crossing_order[stick][position]]:
                            edge_and_next.append(False)
                        if p[stick] == p[Stick_crossing_order[stick][position]]:
                            edge_and_next.append('skip7')
                    if ((stick%2) == 1) and ((Stick_crossing_order[stick][position]%2) == 1):
                        if p[stick] > p[Stick_crossing_order[stick][position]]:
                            edge_and_next.append(True)
                        if p[stick] < p[Stick_crossing_order[stick][position]]:
                            edge_and_next.append(False)
                        if p[stick] == p[Stick_crossing_order[stick][position]]:
                            edge_and_next.append('skip8')

                if stick == Stick_crossing_order[stick][position]:
                    edge_and_next.append('skip9')
                if len(edge_and_next) != 3:
                    edge_and_next.append('skip10') 
                count += 1  
                total[count] = edge_and_next
        temp_vert = []
        verts = []
        for x in range(2*nv):
            verts.append([x%(2*nv), (total[x][0])%(2*nv), (x+1)%(2*nv), (total[x][1])%(2*nv),total[x][2]])
       
        for z in range(2*nv):
            if verts[z][4] == True:
                verts[z][4] = 1
            if verts[z][4] == False:
                verts[z][4] = 0
            if verts[z][4] == 'skip':
                print 'skipped'
                del(verts[z])
                verts.insert(z,[0,0,0,0])
        for t in range(8*nv):
            if (verts[t%(2*nv)][0] <= verts[t%(2*nv)][1]) and (verts[t%(2*nv)][0] <= verts[t%(2*nv)][2] and (verts[t%(2*nv)][0] <= verts[t%(2*nv)][3])):
                continue
            if (verts[t%(2*nv)][0] >= verts[t%(2*nv)][1]) or (verts[t%(2*nv)][0] >= verts[t%(2*nv)][2] or (verts[t%(2*nv)][0] >= verts[t%(2*nv)][3])):
                temp_vert = [verts[t%(2*nv)][1],verts[t%(2*nv)][2],verts[t%(2*nv)][3],verts[t%(2*nv)][0],verts[t%(2*nv)][4]]
                verts[t%(2*nv)] = [temp_vert[0],temp_vert[1],temp_vert[2],temp_vert[3],temp_vert[4]]
        ne = 2*nv 
        for clean_up in range(ne):
            for search in range(ne): 
                if (([verts[clean_up][0], verts[clean_up][1], verts[clean_up][2], verts[clean_up][3]] == [verts[search][0], verts[search][1], verts[search][2], verts[search][3]]) and (clean_up != search)) and ([verts[clean_up][0], verts[clean_up][1], verts[clean_up][2], verts[clean_up][3]] != [0,0,0,0]) :
                    del(verts[search])
                    verts.insert(search,[0,0,0,0])
        count = 0
        for clean_up_2 in range(ne*ne):
            if verts[clean_up_2%ne] == [0,0,0,0]:
                del(verts[clean_up_2%ne])
                verts.append([])
                count = 0
            count += 1
            if count >= (ne+1):
                break
        del(verts[nv:ne])
        for r in range(nv):
            if verts[r][0] == 0 and r != 0 :
               temp = verts[r]
               del(verts[r])
               verts.insert(0,temp)
        print verts
        knot = PlanarDiagram.from_pdcode(verts)
        for v in range(nv):
            knot.crossings[v].sign = verts[v][4]
        return knot
    show = raw_input('Do you want to graph this star? y/n  ')
    if show == 'n':
        a = odd_point_star(k,permutation)
        return a
    if show == 'y':
        a = odd_point_star(k,permutation)
        draw_odd_point_star(k,permutation)
        return  a
    
