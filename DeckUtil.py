#!/usr/bin/env python3


def hstopy(filename): # method used to convert from a .hsdeck format to python list format
    name = "./" + filename + ".hsdeck"
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
    name = "./" + filename + ".hsdeck"
    with open(name, 'w') as file:
        file.write(hero + ',\n')
        for i, element in enumerate(decklist):
            file.write(element)
            if i != len(decklist)-1:
                file.write(',\n')


hero = "mage"
deck = ['Test', 'Deck', 'MurlocRaider', 'MurlocRaider', 'BloodfenRaptor', 'BloodfenRaptor', 'FrostwolfGrunt', 'FrostwolfGrunt', 'RiverCrocolisk', 'RiverCrocolisk', 'IronfurGrizzly', 'IronfurGrizzly', 'MagmaRager', 'MagmaRager', 'SilverbackPatriarch', 'SilverbackPatriarch', 'ChillwindYeti', 'ChillwindYeti', 'OasisSnapjaw', 'OasisSnapjaw', 'SenjinShieldmasta', 'SenjinShieldmasta', 'BootyBayBodyguard', 'BootyBayBodyguard', 'FenCreeper', 'FenCreeper', 'BoulderfistOgre', 'BoulderfistOgre', 'WarGolem', 'WarGolem']
pytohs("testdeck", hero, deck)


def createConfig(filename, deck0, deck1, numberOfRuns): # pass in deck names without the .hsdeck. This method assumes that the simulation uses one ai (ai.hsai)
    name = "./" + filename + ".hsparam"
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


print(getAllCards("mage"))