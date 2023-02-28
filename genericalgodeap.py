#!/usr/bin/env python3
"""
Genetic algorithm implemented with DEAP solving the one max problem
(maximising number of 1s in a binary string).

"""
import random
import statistics

from deap import creator, base, tools, algorithms

#This have to return a tupple dont be dumb
def evaluate(x):
	return (sum(x),)


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=16)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=10)

hof = tools.HallOfFame(3)
stats = tools.Statistics(lambda x: x.fitness.values[0])
stats.register("avg", statistics.mean)
stats.register("std", statistics.stdev)
stats.register("max",max)


population, log = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.1,
	ngen=50, stats=stats, halloffame=hof, verbose=False)

print(log)

print("\nbest 3 global solutions:\n", hof)
print("\nbest 3 in last population:\n", tools.selBest(population, k=3))
