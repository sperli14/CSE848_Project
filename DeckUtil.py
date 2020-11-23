#!/usr/bin/env python3
import random
import os


def hstopy(filename): # method used to convert from a .hsdeck format to python list format
    name = "./HearthSim-master/experiments/" + filename + ".hsdeck"
    with open(name, 'r') as file:
        hero = file.readline().rstrip(",\n")
        allcards = file.read()
        decklist = allcards.split(",\n")

        # print(decklist)

    return hero, decklist
    # file.close()


# hero, deck = hstopy("deck0")
# print(hero)
# print(deck)


def pytohs(filename, hero, decklist): # method used to convert to a .hsdeck format
    name = "./HearthSim-master/experiments/" + filename + ".hsdeck"
    with open(name, 'w') as file:
        file.write(hero + ',\n')
        for element in decklist:
            file.write(element + ',\n')


hero = "mage"
deck = ['Test', 'Deck', 'MurlocRaider', 'MurlocRaider', 'BloodfenRaptor', 'BloodfenRaptor', 'FrostwolfGrunt', 'FrostwolfGrunt', 'RiverCrocolisk', 'RiverCrocolisk', 'IronfurGrizzly', 'IronfurGrizzly', 'MagmaRager', 'MagmaRager', 'SilverbackPatriarch', 'SilverbackPatriarch', 'ChillwindYeti', 'ChillwindYeti', 'OasisSnapjaw', 'OasisSnapjaw', 'SenjinShieldmasta', 'SenjinShieldmasta', 'BootyBayBodyguard', 'BootyBayBodyguard', 'FenCreeper', 'FenCreeper', 'BoulderfistOgre', 'BoulderfistOgre', 'WarGolem', 'WarGolem']
pytohs("testdeck", hero, deck)


def createConfig(filename, deck0, deck1, numberOfRuns): # pass in deck names without the .hsdeck. This method assumes that the simulation uses one ai (ai.hsai)
    name = "./HearthSim-master/experiments/" + filename + ".hsparam"
    with open(name, 'w') as file:

        # IMPORTANT: DO NOT CHANGE THE SPACING
        file.write("num_simulations           =   " + str(numberOfRuns) + "\n")
        file.write("num_threads               =   1" + "\n")
        file.write("\n")

        file.write("output_file               =   " + filename + ".hsres" + "\n")
        file.write("\n")

        file.write("deckListFilePath0         =       " + deck0 + ".hsdeck" + "\n")
        file.write("deckListFilePath1         =       " + deck1 + ".hsdeck" + "\n")
        file.write("\n")

        file.write("aiParamFilePath0          =       " + "ai.hsai" + "\n")
        file.write("aiParamFilePath1          =       " + "ai.hsai" + "\n")
        file.write("\n")


#createConfig("testparam", "deck0", "deck0", 100)


# input classname, returns neutral and class cards
def getAllCards(classname):
    name = "./res/cards/" + classname + ".hsdeck"
    with open(name, 'r') as file:
        temp = file.read()
        cardlist = temp.split(",\n")

    neutral = "./res/cards/noclass.hsdeck"
    with open(neutral, 'r') as file:
        temp = file.read()
        neutralcards = temp.split(",\n")
    return neutralcards + cardlist


mage = random.sample(getAllCards("mage"), 30)
print(mage)
pytohs("mage", "None", mage)

warlord = random.sample(getAllCards("warlord"), 30)
print(warlord)
pytohs("warlord", "None", warlord)

createConfig("config", "mage", "warlord", 10)
os.chdir("./HearthSim-master")
os.system("gradlew runSim")

# import subprocess
# output = subprocess.check_output(os.getcwd() + "/HearthSim-master/gradlew runSim", shell=True)