import json
import multiprocessing
import statistics
import random
from deap import creator, base, tools, algorithms

from PIL import Image, ImageDraw
from PIL import ImageChops

from mutationsUtils import mutate_point, change_color
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

    return image

#Diff kind of mutation I can Try to choose and implement
# (add / update / replace polygon, change points / colour / z-order)
#Don't forget that we re on a image, so all tje triangle are here
def mutate(solution, indpb):

    if random.random() < 0.5:
        # mutate points
        for i in range(10):
            mutate_point(solution,tools,indpb)
    else:
      
            # reorder polygons 

            tools.mutShuffleIndexes(solution, indpb)
            # print("\n\n\n")
            # print(solution)
            # print("\n\n")
            
    #La solution est une liste de polygiones, pour l'instant on a ca
    #[[(123, 81, 206, 59), (103, 171), (69, 184), (179, 37)],...
    return solution,






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


#do some configfiles to note have to change the parameters
def run(generations=500, population_size=100,  seed=31):
# Car c est la plus procche qu'on peut avoir
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)


    random.seed(seed)
    toolbox = base.Toolbox()
    pool = multiprocessing.Pool(8)
    toolbox.register("map", pool.map)
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

    #Create population
    population = toolbox.population( n=population_size)
    hof = tools.HallOfFame(3)
    stats = tools.Statistics(lambda x: x.fitness.values[0])
    stats.register("avg", statistics.mean)
    stats.register("std", statistics.stdev)
    stats.register("max", max)

    population, log = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.1,
        ngen=50, stats=stats, halloffame=hof, verbose=False)


    # main evolution loop
    for g in range(generations):
        print("generation Nanan°"+str(g))

        #2 different approaches here
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.7)
        # offspring = algorithms.varOr(population,toolbox, cxpb=0.5, mutpb=0.5,lambda_=100)
        #Same here, we can check for mu+lambda or mu, lambda but not in this first instance
        fitnesses = toolbox.map(toolbox.evaluate, offspring)
        population = offspring
        for value, individual in zip(fitnesses, offspring):
            individual.fitness.values  = value
        
        population = toolbox.select(population, len(population))


        
    image =draw(population[0])
    image.save("solution.png")
    print(log)
    # print("\nbest 3 in last population:\n", tools.selBest(population, k=3))
    listesol = tools.selBest(population, k=3)
    for a in listesol:
        image =draw(a)
        image.save(str(random.randrange(90))+"solution.png")

#
# Should had halloffames
#should had statistics as well
#
def read_config(path):
       with open(path) as f_in:
        return json.load(f_in)


if __name__ == "__main__":
    # params = read_config(sys.argv[1])
    #If we define the name of attributes greately in the json it will work
    run()
    # run(**params)