import random
from DeckUtil import getAllCards

class CardGenerator():
    def __init__(self):
        self._class_card_dict = {}
        
    #return a random card from the chosen class - includes neutral cards
    def generate_random_card(self, classname):
        if classname not in self._class_card_dict:
            self._class_card_dict[classname] = getAllCards(classname)
        return random.choice(self._class_card_dict[classname])