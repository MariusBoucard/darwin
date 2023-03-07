import json
import multiprocessing
import statistics
import random
from deap import creator, base, tools, algorithms
from IPython.display import display # to display images
from PIL import Image, ImageDraw, ImageTk
from PIL import ImageChops
import sys





from mutationsUtils import mutate_point, change_color,remove_polygon,add_polygone,make_polygon
MAX = 255 * 200 * 200
TARGET = Image.open("5a.png")
caca = Image.open("5c.png")
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
    rand = random.random()
    if rand< 0.8:
        # mutate points
            mutate_point(solution,tools,indpb)
    elif 0.8<rand<0.85:
             tools.mutShuffleIndexes(solution, indpb)
    elif 0.85<rand<0.89 :
    #         # reorder polygons 
             remove_polygon(solution,1)
    elif 0.89<rand<0.95 :
            add_polygone(solution,1)
    elif 0.95<rand<1.0 : 
            change_color(solution,1)
            
    #La solution est une liste de polygiones, pour l'instant ons a ca
    #[[(123, 81, 206, 59), (103, 171), (69, 184), (179, 37)],...
    return solution,








# cross over only when fitness is low 
# perhaps different stages that dynamic change where the fitness is
#do some configfiles to note have to change the parameters
def run(generations=500, population_size=100,  seed=30,polygons=20,mutation_rate=0.9,mating_prob = 0.01):
# Car c est la plus procche qu'on peut avoir
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)


    random.seed(seed)
    toolbox = base.Toolbox()
    pool = multiprocessing.Pool(8)
    toolbox.register("map", pool.map)
    # toolbox.register("mutate", mutate, indpb=0.05)
    toolbox.register("individual", tools.initRepeat, creator.Individual,  make_polygon, n=polygons)
    toolbox.register("population",tools.initRepeat, list, toolbox.individual)
    
    # initialization
    #We need a mate 
    toolbox.register("mate", tools.cxTwoPoint)
    #Record the mutate function
    toolbox.register("mutate", mutate, indpb=0.05)
    #We have to tell him to evaluate the distance between both pictures
    toolbox.register("evaluate", evaluate)
    #Whitch selection algorithm we're using
    toolbox.register("select", tools.selection.selLexicase)

    #Create population
    population = toolbox.population( n=population_size)
    hof = tools.HallOfFame(3)
    stats = tools.Statistics(lambda x: x.fitness.values[0])
    stats.register("avg", statistics.mean)
    stats.register("std", statistics.stdev)
    stats.register("max", max)

    population, log = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=mutation_rate,
        ngen=generations, stats=stats, halloffame=hof, verbose=False)


    # main evolution loop
    for g in range(generations):
        print("generation Nanan°"+str(g))

        #2 different approaches here
        offspring = algorithms.varAnd(population, toolbox, cxpb=mating_prob, mutpb=mutation_rate)
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

def read_config(path):
       with open(path) as f_in:
        return json.load(f_in)


if __name__ == "__main__":
    params = read_config(sys.argv[1])
    #If we define the name of attributes greately in the json it will work
    run()
    # run(**params)