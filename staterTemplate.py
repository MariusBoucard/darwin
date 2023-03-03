import sys
import random
from deap import creator, base, tools, algorithms

from PIL import Image, ImageDraw
from PIL import ImageChops

MAX = 255 * 200 * 200
TARGET = Image.open("5a.png")
TARGET.load()  # read image and close the file


##Don t change it please
def evaluate(solution):
    image = draw(solution)
    diff = ImageChops.difference(image, TARGET)
    hist = diff.convert("L").histogram()
    count = sum(i * n for i, n in enumerate(hist))
    return (MAX - count) / MAX,

#If I want to display other things
def draw(solution):
    image = Image.new("RGB", (200, 200))
    canvas = ImageDraw.Draw(image, "RGBA")
    for polygon in solution:
        canvas.polygon(polygon[1:], fill=polygon[0])

    image.save("solution.png")
    return image


def mutate(solution, indpb):
    if random.random() < 0.5:
        # mutate points
        polygon = random.choice(solution)
        coords = [x for point in polygon[1:] for x in point]
        # tools.mutGaussian(coords, 0, 10, indpb)
        coords = [max(0, min(int(x), 200)) for x in coords]
        polygon[1:] = list(zip(coords[::2], coords[1::2]))
    else:
            # reorder polygons
            tools.mutShuffleIndexes(solution, indpb)
            
    return solution,






def make_polygon():
    # 0 <= R|G|B < 256, 30 <= A <= 60, 10 <= x|y < 190
    minalpha = 30
    maxalpha =60
    mincol = 30
    maxcol = 255
    mincor = 10
    maxcor = 189

    return [(random.randrange(mincol, maxcol), random.randrange(mincol, maxcol), random.randrange(mincol, maxcol), random.randrange(minalpha,maxalpha)),
             (random.randrange(mincor, maxcor), random.randrange(mincor, maxcor)),
               (random.randrange(mincor, maxcor), random.randrange(mincor, maxcor)),
                 (random.randrange(mincor, maxcor), random.randrange(mincor, maxcor))]


#do some configfiles to note have to change the parameters
def run(generations=500, population_size=100,  seed=31):
# Car c est la plus procche qu'on peut avoir
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)


    random.seed(seed)
    toolbox = base.Toolbox()
    # toolbox.register("mutate", mutate, indpb=0.05)
    toolbox.register("individual", tools.initRepeat, creator.Individual,  make_polygon, n=100)
    toolbox.register("population",tools.initRepeat, list, toolbox.individual)
    
    # initialization
    #We need a mate 
    toolbox.register("mate", tools.cxTwoPoint)
    #Record the mutate function
    toolbox.register("mutate", mutate, indpb=0.05)
    #We have to tell him to evaluate the distance between both pictures
    toolbox.register("evaluate", evaluate)
    #Whitch selection algorithm we're using
    toolbox.register("select", tools.selection.selBest)
    population = toolbox.population( n=population_size)

    draw(population[0])

    # main evolution loop
    for g in range(generations):
        print("generation Nanan°"+str(g))
        population = toolbox.select(population, len(population))
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.5)
        fitnesses = toolbox.map(toolbox.evaluate, offspring)
        population = offspring
        for value, individual in zip(fitnesses, offspring):
            individual.fitness.values  = value

        
    draw(population[0])


#
# Should had halloffames
#should had statistics as well
#
def read_config(path):
    # read JSON or ini file, return a dictionary
    pass


if __name__ == "__main__":
    # params = read_config(sys.argv[1])
    #If we define the name of attributes greately in the json it will work
    run()
    # run(**params)