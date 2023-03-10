import datetime
import json
import multiprocessing
import statistics
import random
from deap import creator, base, tools, algorithms
from IPython.display import display # to display images
from PIL import Image, ImageDraw, ImageTk
from PIL import ImageChops
import sys
from mutationsUtils import mutate_point, change_color,remove_polygon,add_polygone,make_polygon, add_point

TARGET_NAME="5b.png"
MAX = 255 * 200 * 200
TARGET = Image.open(TARGET_NAME)
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

#########################################
#
#
#       This mutate function is the core of this evolutional algorithm
#       It allows user to choose the weights of every probability and to choose as well
#       if multiple changes can happen in the same mutation.
#       Be carefull, I've add a check 
#########################################
def mutate(solution, indpb,mutate_pt=0.8,shuffle=0.05,remove_poly=0.02,add_poly=0.05,change_cr=0.03,add_pt=0.05,independance=False):

    if not independance :
        assert int(mutate_pt+shuffle+remove_poly+add_poly+change_cr+add_pt) == 1, "mutations probabilities should sum up to 1" +str(mutate_pt+shuffle+remove_poly+add_poly+change_color+add_pt)
        rand = random.random()
        if rand< mutate_pt:
                mutate_point(solution,tools,indpb)
        elif mutate_pt<rand<(shuffle+mutate_pt):
                tools.mutShuffleIndexes(solution, indpb)
        elif (shuffle+mutate_pt)<rand<(shuffle+mutate_pt+remove_poly) :
  
                remove_polygon(solution,1)
        elif (shuffle+mutate_pt+remove_poly)<rand<(shuffle+mutate_pt+remove_poly+add_poly) :
                add_polygone(solution,1)
        elif (shuffle+mutate_pt+remove_poly+add_poly)<rand<(shuffle+mutate_pt+remove_poly+add_poly+change_cr) : 
                change_color(solution,1)
        else :
            add_point(solution)
    else :
        rand = random.random()
        if rand< mutate_pt:
                mutate_point(solution,tools,indpb)
        if rand<(shuffle):
                tools.mutShuffleIndexes(solution, indpb)
        if rand<remove_poly :
                remove_polygon(solution,1)
        if rand<add_poly :
                add_polygone(solution,1)
        if rand<change_cr : 
                change_color(solution,1)
        if rand<add_pt :
            add_point(solution)

            
    #La solution est une liste de polygiones, pour l'instant ons a ca
    #[[(123, 81, 206, 59), (103, 171), (69, 184), (179, 37)],...
    return solution,








# cross over only when fitness is low 
# perhaps different stages that dynamic change where the fitness is
#do some configfiles to note have to change the parameters
def run(generations=500,generations2=0, population_size=100,  seed=30,polygons=20,mutation_rate=0.9,mating_prob = 0.01
        ,mutate_pt=0.8,shuffle=0.05,remove_poly=0.02,add_poly=0.05,change_cr=0.03,add_pt=0.05,independance=False,
        mutate_pt2=0.8,shuffle2=0.05,remove_poly2=0.02,add_poly2=0.05,change_cr2=0.03,add_pt2=0.05,independance2=False):
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
    print("here for long")
    # initialization
    #We need a mate -> That's our crossover function
    toolbox.register("mate", tools.cxTwoPoint)
    #Record the mutate function
    toolbox.register("mutate", mutate, indpb=0.05,
                     mutate_pt=mutate_pt,shuffle=shuffle,remove_poly=remove_poly,add_poly=add_poly,change_cr=change_cr,add_pt=add_pt,independance=independance)
    #We have to tell him to evaluate the distance between both pictures
    toolbox.register("evaluate", evaluate)
    #Whitch selection algorithm we're using
    toolbox.register("select", tools.selection.selLexicase)
    # toolbox.register("select", tools.selection.selBest)


    #Create population
    population = toolbox.population( n=population_size)
    hof = tools.HallOfFame(3)
    stats = tools.Statistics(lambda x: x.fitness.values[0])
    stats.register("avg", statistics.mean)
    stats.register("std", statistics.stdev)
    stats.register("max", max)
    print("stats sets")
    population, log = algorithms.eaSimple(population, toolbox, cxpb=mating_prob, mutpb=mutation_rate,
        ngen=generations, stats=stats, halloffame=hof, verbose=False)


    # main evolution loop
    for g in range(generations):
        print("generation Nanan°"+str(g))

        #2 different approaches here
        # offspring = algorithms.varAnd(population, toolbox, cxpb=mating_prob, mutpb=mutation_rate)       
        offspring = algorithms.varOr(population,toolbox, cxpb=mating_prob, mutpb=mutation_rate,lambda_=100)
        #Same here, we can check for mu+lambda or mu, lambda but not in this first instance
        fitnesses = toolbox.map(toolbox.evaluate, offspring)
        population = offspring
        for value, individual in zip(fitnesses, offspring):
            individual.fitness.values  = value
        
        population = toolbox.select(population, len(population))

    if generations2 !=0 :
           toolbox.register("mutate", mutate, indpb=0.05,
                     mutate_pt=mutate_pt2,shuffle=shuffle2,remove_poly=remove_poly2,add_poly=add_poly2,change_cr=change_cr2,add_pt=add_pt2,independance=independance2)    
           for g in range(generations2):
                print("generation 2 Nanan°"+str(g))

                offspring = algorithms.varAnd(population, toolbox, cxpb=mating_prob, mutpb=mutation_rate)       
                # offspring = algorithms.varOr(population,toolbox, cxpb=0.5, mutpb=0.5,lambda_=100)
                #Same here, we can check for mu+lambda or mu, lambda but not in this first instance
                fitnesses = toolbox.map(toolbox.evaluate, offspring)
                population = offspring
                for value, individual in zip(fitnesses, offspring):
                        individual.fitness.values  = value
          

    list1 = tools.selLexicase(population,1)
    for a in list1:
        
        image =draw(a)
        image.save("solution.png")
    print(log)
    # print("\nbest 3 in last population:\n", tools.selBest(population, k=3))
    listesol =     tools.selLexicase(population,3)

    for a in listesol:
        image =draw(a)
        image.save(str(random.randrange(90))+"solution.png")

    f = open("ExecutionReport-"+str(datetime.datetime.now())+".txt", "x") 
    f.write(
          "Execution of the code with theses parameters\n"+
          "On this image bro "+TARGET_NAME+
         
        "\ngenerations : " +str(generations)+
        "\ngenerations2 :"+str(generations2)+
        "\npopulation_size :"+str(population_size)+
        "\nseed : "+str(seed),
        "\npolygons :"+str(polygons)+
        "\nmutation_rate :"+str(mutation_rate)+
        "\nmating_prob : "+str(mating_prob),
        "\nmutate_pt :"+str(mutate_pt)+
        "\nshuffle :"+str(shuffle)+
        "\nremove_poly :"+str(remove_poly)+
        "\nadd_poly :"+str(add_poly)+
        "\nchange_cr :"+str(change_cr)+
        "\nadd_pt :"+str(add_pt)+
        "\nindependance :"+str(False)+
        "\nmutate_pt2 :"+str(mutate_pt2)+
        "\nshuffle2 :"+str(shuffle2)+
        "\nremove_poly2"+str(remove_poly2)+
        "\nadd_poly2 :"+str(add_poly2)+
        "\nchange_cr2 :"+str(change_cr2)+
        "\nadd_pt2 :"+str(add_pt2)+
        "\nindependance2 :"+str(False)
         +
         "We got theses results \n"+
        str(log)
    )
    f.close
#
# Should had halloffames
#should had statistics as well

def read_config(path):
       with open(path) as f_in:
        return json.load(f_in)


if __name__ == "__main__":
    params = read_config(sys.argv[1])
    #If we define the name of attributes greately in the json it will work
    run(**params)
    # run(**params)