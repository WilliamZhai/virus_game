from utilities import Chance


class Player:

    def __init__(self, name, health, max_food, food, hunger):
        self.name = name
        self.health = health
        self.max_food = max_food
        self.food = food
        self.hunger = hunger

        self.viruses = []
        self.score = 0

    def is_alive(self):
        return self.health > 0

    def add_virus(self, new_virus):
        self.viruses.append(new_virus)

    def add_food(self, amount):
        self.food = min(self.food + amount, self.max_food)

    def process(self):
        # food
        if self.food == 0:
            self.health = self.health - self.hunger
        else:
            self.food = self.food - 1

        # viruses
        for virus in self.viruses:
            # damage from virus
            if Chance.get_random(virus.get_current_severe_chance()):
                self.lose_health(virus.damage)
                # todo: remove virus?

            # process our virus - aging
            virus.process()
            if not virus.is_live():
                self.viruses.remove(virus)

    def lose_health(self, amount):
        self.health = self.health - amount

    def increase_score(self, amount):
        self.score = self.score + amount
