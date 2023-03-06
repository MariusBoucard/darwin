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