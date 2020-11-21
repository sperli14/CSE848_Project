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