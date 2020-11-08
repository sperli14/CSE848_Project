import random
from operator import itemgetter
from os import system

#change properties file then run:
#gradle runSim
deck_id = 0

def random_card():
    pass

def initialization(N):
    population = []
    for i in range(N):
        deck = []
        for j in range(30):#30 card decks
            found = False
            while not found:
                card = random_card()
                if deck.count(card) <= 1:
                    deck.append(card)
                    found = True
        population.append(deck)
    return population

#take in one model and swap out one card for another
def mutate(model):
    pos = random.randint(0,len(model))
    found = False
    while not found:
        card = random_card()
        if model.count(card) <= 1:
            model[pos] = card
            found = True
    return model

#performs simple recombination from two models using crossover
#not done
#only two copies of a card per deck, 1 if legendary
def recombination(model1, model2):
    crossover_point = random.randint(1,len(model1))
    child1 = model1[:crossover_point]# + model2[crossover_point:]
    for i in range(crossover_point, len(model2)):
        if child1.count(model2[i]) <= 1:
            child1.append(model2[i])
    child2 = model2[:crossover_point] + model1[crossover_point:]
    return child1, child2
    
def fitness(model):
    pass

#performs parent and survivor selection
#also performs recombination by calling the previous function
def selection(population):
    #evaluate population
    models_fitness = []
    for model in population:
        models_fitness.append((model,fitness(model)))
    #models_fitness.sort(key=itemgetter(1), reverse=True)
    
    #birth new models
    for i in range(len(population)):
        #five random members selected, best two get to breed
        chosen = random.sample(models_fitness, 5)
        chosen.sort(key=itemgetter(1), reverse=True)
        parents = chosen[:2]
        offspring1, offspring2 = recombination(parents[0][0], parents[1][0])
        #evaluate offspring
        offspring1_fitness = fitness(offspring1)
        offspring2_fitness = fitness(offspring2)
        models_fitness.append((offspring1, offspring1_fitness))
        models_fitness.append((offspring2, offspring2_fitness))
    
    
    models_fitness.sort(key=itemgetter(1), reverse=True)
    
    #SUS with elitism
    models_fitness = [models_fitness[i] for i in range(0, len(models_fitness), 3)]
    population = [model_tup[0] for model_tup in models_fitness]
    
    return population

def build_deck_file(model):
    outfile = open(str(deck_id)+".hsdeck", 'w')
    deck_class = "None"
    outfile.write(deck_class)
    for card in model:
        outfile.write(",\n")
        outfile.write(card)
    outfile.close()
    #deck_id+=1


def hearthstone_GA():
    pop_size = 500
    population = initialization(pop_size)
    best_fitness = -1000000
    best_model = None
    fitness_evals = 0
    generation = 0
    fitnesses = []
    #each iteration of this loop is a generation
    while generation < 1000:
        generation += 1
        fitness_evals += 1500#each generation performs 1500 fitness evaluations
        population = selection(population)
        index = 0
        while index < 500:
            model = population[index]
            roll = random.random()
            #80% chance of mutation for each member of the population
            if roll < 0.80:
                population[index] = mutate(model)
            index += 1
        #evaluate and find best model
        models_fitness = []
        for model in population:
            models_fitness.append((model,fitness(model)))
        models_fitness.sort(key=itemgetter(1), reverse=True)
        fitnesses.append(models_fitness[0][1])
        if models_fitness[0][1] > best_fitness:
            best_fitness = models_fitness[0][1]
            best_model = models_fitness[0][0]
    #after termination condition, display best model, best fitness of said model, how many generations ran, and how many fitness evaluations
    print(best_model)
    print(best_fitness)
    print("Generation:", generation)
    print("Fitness Evals:", fitness_evals)