import math


class Virus:

    def __init__(self, name, total_length, infection_chance, severe_chance, damage, decay_rate=0.5):
        """
        The virus @name will last @length rounds, beginning with @infection_chance.
        @infection_chance will have a half-life decay every round. Once the @infection_chance
        reaches the infection_floor the virus is gone.
        """
        self.name = name
        self.total_length = total_length
        self.base_infection_chance = infection_chance
        self.base_severe_chance = severe_chance

        self.damage = damage
        self.decay_rate = decay_rate
        self.day = 0

    def is_live(self):
        return self.day <= self.total_length

    def get_current_infection_chance(self):
        return self.base_infection_chance

    def get_current_severe_chance(self):
        severe_day = 2  # after day 2 the severe chance will decrease
        if self.day <= severe_day:
            return self.base_severe_chance
        else:
            return self.base_severe_chance * math.pow(self.decay_rate, self.day - severe_day)

    def process(self):
        if self.day < self.total_length:
            self.day = self.day + 1
