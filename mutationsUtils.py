import random


def change_color(solution,nbPolygones=1):
        minalpha = 30
        maxalpha =60
        mincol = 30
        maxcol = 255
        # change color of polynome
        for i in range(nbPolygones):
    
                polygon = random.choice(solution)
                polygon[0]=((random.randrange(mincol, maxcol), random.randrange(mincol, maxcol), random.randrange(mincol, maxcol), random.randrange(minalpha,maxalpha)))

def mutate_point(solution,tools,indpb):
        polygon = random.choice(solution)
        coords = [x for point in polygon[1:] for x in point]
        tools.mutGaussian(coords, 0, 10, indpb)
        coords = [max(0, min(int(x), 200)) for x in coords]
        polygon[1:] = list(zip(coords[::2], coords[1::2]))

def add_polygone(solution,nbPolygones) :
        for i in range(nbPolygones) :
                solution.append(make_polygon())

def remove_polygon(solution,nbPolygones=1):
        if  len(solution) < nbPolygones :
        # change color of polynome
                for i in range(nbPolygones):
                        polygon = random.choice(solution)
                        solution.remove(polygon)
        else: 
                add_polygone(solution,random.randint(2,14))

def make_polygon():
    # 0 <= R|G|B < 256, 30 <= A <= 60, 10 <= x|y < 190
    minalpha = 30
    maxalpha =60
    mincol = 0
    maxcol = 255
    mincor = 10
    maxcor = 189
    

    return [(random.randrange(mincol, maxcol), random.randrange(mincol, maxcol), random.randrange(mincol, maxcol), random.randrange(minalpha,maxalpha)),
             (random.randrange(mincor, maxcor), random.randrange(mincor, maxcor)),
               (random.randrange(mincor, maxcor), random.randrange(mincor, maxcor)),
                 (random.randrange(mincor, maxcor), random.randrange(mincor, maxcor))]

#TODO : add a point into the polygon -> See the slides for not doing shit


def add_point(solution) : 
        polygon = random.choice(solution)
        polypoints = polygon[1:]

        #Calculating the center of mass of the polygon : 
        xmass = 0
        ymass =0
        for points in polypoints :
                xmass += points[0]
                ymass += points[1]
        xmass = xmass/len(polypoints)
        ymass = ymass/len(polypoints)

        #Creating the vectors
        vectors = []
        for points in polypoints :
                vect = (points[0]-xmass,points[1]-ymass)



