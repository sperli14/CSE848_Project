import random
from operator import itemgetter, attrgetter
from os import system
from DeckUtil import pytohs, createConfig
from HSdeck import HSdeck
from CardGenerator import CardGenerator

#change properties file then run:
#gradle runSim
cardGenerator = CardGenerator()

def initialization(N):
    population = []
    classname = "mage"
    for i in range(N):
        deck = []
        for j in range(30):#30 card decks
            found = False
            while not found:
                card = cardGenerator.generate_random_card(classname)
                if deck.count(card) <= 1:
                    deck.append(card)
                    found = True
        population.append(HSdeck(classname, deck))
    return population

#take in one model and swap out one card for another
def mutate(model):
    classname = model.get_class()
    deck = model.get_deck()
    pos = random.randint(0,len(deck))
    found = False
    while not found:
        card = cardGenerator.generate_random_card(classname)
        if deck.count(card) <= 1:
            deck[pos] = card
            found = True
    model.set_deck(deck)

#performs simple recombination from two models using crossover
#not done
#only two copies of a card per deck, 1 if legendary
def recombination(model1, model2):
    classname = model1.get_class()
    deck1 = model1.get_deck()
    deck2 = model2.get_deck()
    crossover_point = random.randint(1,len(deck1))
    child_deck1 = deck1[:crossover_point]
    for i in range(crossover_point, len(deck2)):
        if child_deck1.count(deck2[i]) <= 1:
            child_deck1.append(deck2[i])
    child_deck2 = deck2[:crossover_point] + deck1[crossover_point:]
    
    child1 = HSdeck(classname, child_deck1)
    child2 = HSdeck(classname, child_deck2)
    
    return child1, child2

#measures fitness of an individual by having it play against 10 opponents
#winrate is the fitness
#NOT COMPLETE
def fitness(model, population):
    model.set_fitness(0)###################
    return##############################
    games = 10
    adversaries = random.sample(range(len(population)), games)
    wins = 0
    pytohs("deck0", model.get_class(), model.get_deck())
    for index in adversaries:
        opponent = population[index]
        pytohs("deck1", opponent.get_class(), opponent.get_deck())
        createConfig("config", "deck0", "deck1", 1)
        #play a game between model and opponent
        #if model wins, increase wins by one
    fit = wins/games
    model.set_fitness(fit)
    return fit

#record fitness for all population
def fitness_all(population):
    max_fitness = 0
    for i, model in enumerate(population):
        if i != len(population)-1:
            fit = fitness(model, population[:i]+population[i+1:])
        else:
            fit = fitness(model, population[:i])
        if fit > max_fitness:
            max_fitness = fit
    return max_fitness
    

#performs parent and survivor selection
#also performs recombination by calling the previous function
def selection(population):
    #evaluate population
    fitness_all(population)

    offspring = []
    #birth new models
    for i in range(len(population)):
        #five random members selected, best two get to breed
        chosen = random.sample(population, 5)
        chosen.sort(key=attrgetter('fitness'), reverse=True)
        parents = chosen[:2]
        offspring1, offspring2 = recombination(parents[0][0], parents[1][0])
        #evaluate offspring
        fitness(offspring1, population)
        fitness(offspring2, population)
        offspring.append(offspring1)
        offspring.append(offspring2)
    population = population + offspring
    
    population.sort(key=attrgetter('fitness'), reverse=True)
    
    #SUS with elitism
    population = [population[i] for i in range(0, len(population), 3)]    
    return population

"""
def build_deck_file(model):
    outfile = open(str(deck_id)+".hsdeck", 'w')
    deck_class = "None"
    outfile.write(deck_class)
    for card in model:
        outfile.write(",\n")
        outfile.write(card)
    outfile.close()
    #deck_id+=1
"""

def hearthstone_GA():
    pop_size = 100
    population = initialization(pop_size)
    best_fitness = 0
    best_model = None
    fitness_evals = 0
    generation = 0
    fitnesses = []
    #each iteration of this loop is a generation
    while generation < 1000:
        generation += 1
        fitness_evals += 100#each generation performs 100 fitness evaluations
        population = selection(population)
        index = 0
        while index < pop_size:
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