#!/usr/bin/env python3
"""
Genetic algorithm implemented with Evol solving the one max problem
(maximising number of 1s in a binary string).

"""
import random

from evol import Population, Evolution


def initialize():
  return [random.choice([0, 1]) for i in range(16)]


def evaluate(x):
  return sum(x)


def select(population):
  return [random.choice(population) for i in range(2)]


def combine(*parents):
  return [a if random.random() < 0.5 else b for a, b in zip(*parents)]


def flip(x, rate):
  return [1 ^ i if random.random() < rate else i for i in x]


population = Population.generate(initialize, evaluate, size=10, maximize=True)
population.evaluate()

evolution = (Evolution().survive(fraction=0.5)
  .breed(parent_picker=select, combiner=combine)
  .mutate(mutate_function=flip, rate=0.1)
  .evaluate())

for i in range(50):
  population = population.evolve(evolution)
  print("i =", i, " best =", population.current_best.fitness,
    " worst =", population.current_worst.fitness)
