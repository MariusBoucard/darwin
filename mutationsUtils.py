import random
import numpy as np

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
        x_mass = 0
        y_mass =0
        for points in polypoints :
                x_mass += points[0]
                y_mass += points[1]
        x_mass = x_mass/len(polypoints)
        y_mass = y_mass/len(polypoints)

        base_point_rang = random.randint(1,len(polypoints)-1)
        new_point = (polypoints[base_point_rang][0]-polypoints[base_point_rang-1][0],
                     polypoints[base_point_rang][1]-polypoints[base_point_rang-1][1])
        #Creating the vectors
        new_vect = [new_point[0]-x_mass,new_point[1]-y_mass]
        vectors = []
        for points in polypoints :
                vect = [points[0]-x_mass,points[1]-y_mass]
                vectors.append(vect)
        itsok = False
        for i in range(len(polypoints)-1) :
                if (np.angle(vectors[i])[0]<np.angle(new_vect))[0] and (np.angle(vectors[i+1])[0]>np.angle(new_vect)[0]):
                        polypoints.insert(i,new_point)
                        itsok = True
                        break
        if not itsok:
                polypoints.append(new_point)
[0]


