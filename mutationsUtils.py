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
    firsttuple =  (random.randrange(mincor, maxcor), random.randrange(mincor, maxcor))
    #Try to set maximum size for the created triangle
    secondtuple = ()
    thirdtuple = ()


    if firsttuple[0] > (maxcor/2):
        if firsttuple[1]>(maxcor/2):
               secondtuple = (random.randrange(firsttuple[0]-(maxcor/2), firsttuple[0]), random.randrange(firsttuple[1]-(maxcor/2), firsttuple[1]))
               thirdtuple = (random.randrange(firsttuple[0]-(maxcor/2), firsttuple[0]), random.randrange(firsttuple[1]-(maxcor/2), firsttuple[1]))
        else :
                secondtuple = (random.randrange(firsttuple[0]-(maxcor/2), firsttuple[0]), random.randrange( firsttuple[1]),firsttuple[1]+(maxcor/2))
                thirdtuple = (random.randrange(firsttuple[0]-(maxcor/2), firsttuple[0]), random.randrange( firsttuple[1],firsttuple[1]+(maxcor/2)))
    else :
           if firsttuple[1]>(maxcor/2):
               secondtuple = (random.randrange( firsttuple[0],firsttuple[0]+(maxcor/2)), random.randrange(firsttuple[1]-(maxcor/2), firsttuple[1]))
               thirdtuple = (random.randrange( firsttuple[0],firsttuple[0]+(maxcor/2)), random.randrange(firsttuple[1]-(maxcor/2), firsttuple[1]))
           else :
                secondtuple = (random.randrange( firsttuple[0],firsttuple[0]+(maxcor/2)), random.randrange( firsttuple[1]),firsttuple[1]+(maxcor/2))
                thirdtuple = (random.randrange( firsttuple[0],firsttuple[0]+(maxcor/2)), random.randrange( firsttuple[1],firsttuple[1]+(maxcor/2)))
            

    return [(random.randrange(mincol, maxcol), random.randrange(mincol, maxcol), random.randrange(mincol, maxcol), random.randrange(minalpha,maxalpha)),
            firsttuple,
              secondtuple,
                 thirdtuple]