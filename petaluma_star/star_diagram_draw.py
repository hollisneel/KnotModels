# Drawing Star Diagrams
import math, pylab, matplotlib, numpy
from mpl_toolkits.mplot3d import proj3d

def draw_odd_point_star(k, *permutations):
    # This has serious issues correctly displaying the knot. 
    # This needs to be correctly displayed in 3-space.
    # The problem is that matplotlib doesn't work well in 3-space 

    if permutations == ():
        permutation = numpy.random.permutation(k)
    if permutations != ():
        permutation = permutations[0]
    points = []
    lines  = []
    for p in range(k):
        points.append((math.cos((2*(3.14159)*p)/k),math.sin((2*(3.14159)*p)/k)))
    for j in range(len(points)):
        l = j*((k-1)/2)%k
        lines.append([points[l],points[(l+(k-1)/2)%k]])
    fig = matplotlib.pyplot.figure()
    ax  = fig.add_subplot(111, projection = '3d')
    for h in range(k):
        ax.plot([lines[h][0][0],lines[h][1][0]],[lines[h][0][1],lines[h][1][1]],permutation[h],'k',linewidth=3)
        ax.plot([lines[h][0][0],lines[h][1][0]],[lines[h][0][1],lines[h][1][1]],permutation[h],'w',linewidth=1)
        ax.plot([lines[h][0][0],lines[h][0][0]],[lines[h][0][1],lines[h][0][1]],[permutation[h],permutation[(h-1)%k]],'k',linewidth=3)
        ax.plot([lines[h][0][0],lines[h][0][0]],[lines[h][0][1],lines[h][0][1]],[permutation[h],permutation[(h-1)%k]],'w',linewidth=1)
        ax.scatter(lines[h][0][0],lines[h][0][1],permutation[h],c='k')
        ax.scatter(lines[h][0][0],lines[h][0][1],permutation[(h-1)%k],c='k')
    def orthogonal_proj(zfront, zback):
        a = (zfront+zback)/(zfront-zback)
        b = -2*(zfront*zback)/(zfront-zback)
        return numpy.array([[1,0,0,0],
                   [0,1,0,0],
                   [0,0,a,b],
                   [0,0,0,zback]])
    proj3d.persp_transformation = orthogonal_proj
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
