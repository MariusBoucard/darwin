import random
import numpy as np
from PIL import Image, ImageDraw, ImageTk
from PIL import ImageChops
from deap import creator, base, tools, algorithms




def evaluate(solution):
    image = draw(solution)
    diff = ImageChops.difference(image, TARGET)
    hist = diff.convert("L").histogram()
    count = sum(i * n for i, n in enumerate(hist))
    return (MAX - count) / MAX,

TARGET_NAME="5b.png"
MAX = 255 * 200 * 200
TARGET = Image.open(TARGET_NAME)
TARGET.load() 
toolbox = base.Toolbox()
toolbox.register("evaluate", evaluate)

def draw(solution):
    image = Image.new("RGB", (200, 200))
    canvas = ImageDraw.Draw(image, "RGBA")
    for polygon in solution:
        canvas.polygon(polygon[1:], fill=polygon[0])
    return image

def change_color(solution,nbPolygones=1):
        sol2=solution
        fitness_pre = evaluate(solution)
        minalpha = 30
        maxalpha =60
        mincol = 30
        maxcol = 255
        # change color of polynome
        for i in range(nbPolygones):
    
                polygon = random.choice(solution)
                polygon[0]=((random.randrange(mincol, maxcol), random.randrange(mincol, maxcol), random.randrange(mincol, maxcol), random.randrange(minalpha,maxalpha)))
        fitness_post = evaluate(solution)
        if fitness_pre>fitness_post:
               solution=sol2
def mutate_point(solution,tools,indpb):
        sol2=solution
        fitness_pre = evaluate(solution)
        polygon = random.choice(solution)

        coords = [x for point in polygon[1:] for x in point]
        tools.mutGaussian(coords, 0, 10, indpb)
        coords = [max(0, min(int(x), 200)) for x in coords]
        polygon[1:] = list(zip(coords[::2], coords[1::2]))
        fitness_post = evaluate(solution)
        if fitness_pre>fitness_post:
               solution=sol2

def add_polygone(solution,nbPolygones) :
        sol2=solution
        fitness_pre = evaluate(solution)
        for i in range(nbPolygones) :
                solution.append(make_polygon())
        fitness_post = evaluate(solution)
        if fitness_pre>fitness_post:
               solution=sol2

def remove_polygon(solution,nbPolygones=1):
        sol2=solution
        fitness_pre = evaluate(solution)
        if  len(solution) < nbPolygones :
        # change color of polynome
                for i in range(nbPolygones):
                        polygon = random.choice(solution)
                        solution.remove(polygon)
        else: 
                add_polygone(solution,random.randint(2,14))
        fitness_post = evaluate(solution)
        if fitness_pre>fitness_post:
               solution=sol2

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

def make_ellipse():
        minalpha = 30
        maxalpha =60
        mincol = 0
        maxcol = 255
        mincor = 10
        maxcor = 189
        x_0=random.randrange(mincor, maxcor)
        y_0=random.randrange(mincor, maxcor)
        x_1=random.randrange(x_0, maxcor)
        y_1=random.randrange(y_0, maxcor)
        
        return[(random.randrange(mincol, maxcol), random.randrange(mincol, maxcol), random.randrange(mincol, maxcol), random.randrange(minalpha,maxalpha)),
               (x_0,y_0,x_1,y_1)]

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


