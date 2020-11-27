import random
from operator import itemgetter, attrgetter
from os import system, chdir
from DeckUtil import pytohs, createConfig, getResults
from HSdeck import HSdeck
from CardGenerator import CardGenerator
import copy
from statistics import mean
import subprocess

#change properties file then run:
#gradle runSim
cardGenerator = CardGenerator()
chdir("HearthSim-master")


def init(count, classname):
    population = []
    for i in range(count):
        tempdeck = []
        for j in range(30):
            found = False
            while not found:
                card = cardGenerator.generate_random_card(classname)
                if tempdeck.count(card) <= 1:
                    tempdeck.append(card)
                    found = True
        population.append(HSdeck(classname, tempdeck))
    return population


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
    pos = random.randint(0, len(deck)-1)
    found = False
    while not found:
        card = cardGenerator.generate_random_card(classname)
        if deck.count(card) <= 1:
            deck[pos] = card
            found = True
    model.set_deck(deck)
    model.validate()

#performs simple recombination from two models using crossover
#not done
#only two copies of a card per deck, 1 if legendary
def recombination(model1, model2):
    classname = model1.get_class()
    deck1 = model1.get_deck()
    deck2 = model2.get_deck()
    crossover_point = random.randint(0,len(deck1)-1)
    child_deck1 = deck1[:crossover_point]
    for i in range(crossover_point, len(deck2)):
        if child_deck1.count(deck2[i]) <= 1:
            child_deck1.append(deck2[i])
    child_deck2 = deck2[:crossover_point] + deck1[crossover_point:]
    
    child1 = HSdeck(classname, child_deck1)
    child1.validate()
    child2 = HSdeck(classname, child_deck2)
    child2.validate()
    
    return child1, child2

#measures fitness of an individual by having it play against 10 opponents
#winrate is the fitness
def fitness(model, population):
    games = 5
    adversaries = random.sample(range(len(population)), games)
    wins = 0
    #pytohs("deck0", model.get_class(), model.get_deck())
    pytohs("deck0", "Mage", model.get_deck())
    for index in adversaries:
        opponent = population[index]
        #pytohs("deck1", opponent.get_class(), opponent.get_deck())
        pytohs("deck1", "Mage", opponent.get_deck())
        
        system("gradlew runSim")#run simulation
        #if getResults("config")["P0"] == 1:
        #    wins += 1
        with open("experiments/config.hsres") as fp:
            text = fp.read()
            print("run")
            if text[text.index('winner":')+8] == "0":
                wins += 1
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


def removeDeck(iterable, item):
    for i, o in enumerate(iterable):
        if o.get_deck() == item.get_deck():
            del iterable[i]
            break
    return iterable


#plays the deck against x number of random decks in population
def getFitness(deck, population):
    numOfGames = 5
    wins = 0
    tempPop = copy.deepcopy(population)
    all_decks = []
    for subPop in tempPop:
        for element in subPop:
            all_decks.append(element)
    # print(deck)
    # print(all)
    # all.remove(deck)
    removeDeck(all_decks, deck)

    opponents = random.sample(range(len(population)), numOfGames) # list of opponent by index
    #results = []

    pytohs("protagonist", deck.get_class(), deck.get_deck())
    for game in opponents:
        opponent = all_decks[game]
        pytohs("antagonist", opponent.get_class(), opponent.get_deck())

        system("gradlew runSim")

        ##si = subprocess.STARTUPINFO()
        ##si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # si.wShowWindow = subprocess.SW_HIDE # default
        ##subprocess.call('taskkill /F /IM exename.exe', startupinfo=si)

        # results.append(getResults("experiments")["P0"])
        #wins = 0
        fp =  open("experiments/experiments.hsres")
        text = fp.read()
        # print("run")
        while text.find('winner":') == -1:
            system("gradlew runSim")
            fp = open("experiments/experiments.hsres")
            text = fp.read()
        if text[text.find('winner":')+8] == "0":
            wins += 1
        fp.close()
        #results.append(wins/5) #number depends on config file

    return wins/numOfGames#mean(results)


def calculateFitness(population):
    for subPopulation in population:
        for deck in subPopulation:
            deck.set_fitness(getFitness(deck, population))


def tournamentSelection(inp, tournamentSize):  #returns 2 individuals via tournament selection (cannot be same)
    individuals = copy.deepcopy(inp)

    round1 = random.sample(individuals, tournamentSize)

    result1 = round1[0]
    for i in range(len(round1)):
        if round1[i].get_fitness() > result1.get_fitness():
            result1 = round1[i]  #return the greatest individual from round1 sample

    individuals.remove(result1)

    round2 = random.sample(individuals, tournamentSize)

    result2 = round2[0]
    for i in range(len(round2)):
        if round2[i].get_fitness() > result2.get_fitness():
            result2 = round2[i]  # return the greatest individual from round1 sample

    return result1, result2


def crossoverPopulation(population):
    numOfRecombinations = 3  # number of offsprings per class
    populationSize = len(population[0])
    for subPopulation in population:  # append new children to subpopulations
        for i in range(numOfRecombinations):
            ind1, ind2 = tournamentSelection(subPopulation, 3)  #tournament size of 3, hardcoded (can be dynamically allocated later)
            child1, child2 = recombination(ind1, ind2)
            subPopulation.append(child1)
            subPopulation.append(child2)

    calculateFitness(population)  # get new fitness for the new members of the population

    for subPopulation in population:
        subPopulation.sort(key=attrgetter("fitness"), reverse=True)  #

        # cull the population back down to original population size
        cullPop = random.sample(subPopulation[1:], len(subPopulation) - populationSize)
        for i in range(len(cullPop)):
            subPopulation = removeDeck(subPopulation, cullPop[i])
            # subPopulation.remove(i)

    return population

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
        offspring1, offspring2 = recombination(parents[0], parents[1])
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


def save(population, generation):
    with open("savefile.txt", 'w') as file:
        for model in population:
            file.write(model.get_class() + " Fitness:" + str(model.get_fitness()) + ',\n')
            for i, element in enumerate(model.get_deck()):
                file.write(element)
                if i != 29:
                    file.write(',\n')
            file.write("\n\n")
        file.write("Generation:"+str(generation))


def load():
    pass
        

def hearthstone_GA():
    createConfig("experiments", "protagonist", "antagonist", 1)
    pop_size = 5

    # warlordPop = init(pop_size, "warlord")
    # magePop = init(pop_size, "mage")
    # druidPop = init(pop_size, "druid")
    # hunterPop = init(pop_size, "hunter")
    # paladinPop = init(pop_size, "paladin")
    # priestPop = init(pop_size, "priest")
    # roguePop = init(pop_size, "rogue")
    # shamanPop = init(pop_size, "shaman")
    # warriorPop = init(pop_size, "warrior")
    #
    # population = {
    #     "warlord": warlordPop,
    #     "druid": druidPop,
    #     "mage": magePop,
    #     "hunter": hunterPop,
    #     "paladin": paladinPop,
    #     "priest": priestPop,
    #     "rogue": roguePop,
    #     "shaman": shamanPop,
    #     "warrior": warriorPop
    # }
    population = []
    population.append(init(pop_size, "Warlock"))
    population.append(init(pop_size, "Mage"))
    population.append(init(pop_size, "Druid"))
    population.append(init(pop_size, "Hunter"))
    population.append(init(pop_size, "Paladin"))
    population.append(init(pop_size, "Priest"))
    population.append(init(pop_size, "Rogue"))
    population.append(init(pop_size, "Shaman"))
    population.append(init(pop_size, "Warrior"))

    # warlordPop = init(pop_size, "warlord")
    # magePop = init(pop_size, "mage")
    # druidPop = init(pop_size, "druid")
    # hunterPop = init(pop_size, "hunter")
    # paladinPop = init(pop_size, "paladin")
    # priestPop = init(pop_size, "priest")
    # roguePop = init(pop_size, "rogue")
    # shamanPop = init(pop_size, "shaman")
    # warriorPop = init(pop_size, "warrior")

    calculateFitness(population) #give each member of the population a fitness
    print(str(population[0][0]))
    # population = initialization(pop_size)
    # best_fitness = 0
    # best_model = None
    # fitness_evals = 0

    generation = 0
    fitnesses = []
    #each iteration of this loop is a generation
    while generation < 50:
        # save(population, generation)
        generation += 1
        # fitness_evals += 100#each generation performs 100 fitness evaluations

        #cross over population
        population = crossoverPopulation(population)

        #mutate population
        for subPopulation in population:
            for element in subPopulation:
                if random.random() < 0.8:
                    mutate(element)

        #
        # index = 0
        # while index < pop_size:
        #     model = population[index]
        #     roll = random.random()
        #     #80% chance of mutation for each member of the population
        #     if roll < 0.80:
        #         mutate(model)
        #     index += 1
        #evaluate and find best model
        """
        models_fitness = []
        for model in population:
            models_fitness.append((model,fitness(model)))
        models_fitness.sort(key=itemgetter(1), reverse=True)
        fitnesses.append(models_fitness[0][1])
        if models_fitness[0][1] > best_fitness:
            best_fitness = models_fitness[0][1]
            best_model = models_fitness[0][0]"""
    #after termination condition, display best model, best fitness of said model, how many generations ran, and how many fitness evaluations
    # print(best_model)
    # print(best_fitness)

    for subPopulation in population:
        subPopulation.sort(key=attrgetter('fitness'), reverse=True)
        bestIndividual = subPopulation[0]
        print(str(bestIndividual))
        pytohs(bestIndividual.get_class(), bestIndividual.get_class(), bestIndividual.get_deck()) #outputs the best performing individual to heroclass.hsdeck to analyse
        print(str(bestIndividual.get_class()) + "'s best individual has a fitness of: " + str(bestIndividual.get_fitness()))

    print("Generation:", generation)


hearthstone_GA()
