class Location:

    def __init__(self, name, x_position=0, y_position=0, food=5):
        self.name = name
        self.x_position = x_position
        self.y_position = y_position
        self.viruses = []
        self.food = food

    def get_virus_list(self):
        return self.viruses

    def add_virus(self, virus):
        self.viruses.append(virus)

    def get_food(self):
        return self.food

    def process(self):
        for virus in self.viruses:
            if virus.is_live():
                virus.process()
            else:
                self.viruses.remove(virus)
