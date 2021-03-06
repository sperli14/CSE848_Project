class HSdeck():
    def __init__(self, my_class, my_deck=[]):
        self._class = my_class
        self._deck = my_deck
        self.fitness = 0
    def get_deck(self):
        return self._deck
    def get_class(self):
        return self._class
    def set_deck(self, deck):
        self._deck = deck
    def set_fitness(self, fitness):
        self.fitness = fitness
    def get_fitness(self):
        return self.fitness
    def validate(self):
        if len(self._deck) > 30:
            self._deck = self._deck[:30]
    def __str__(self):
        result = self._class + "\n"
        for card in self._deck:
            result += card
            result += "\n"
        result += "Fitness:" + str(self.fitness)
        return result
    def __repr__(self):
        return self.__str__()