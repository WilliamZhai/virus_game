import queue
from termcolor import colored

from src.utilities import Chance
from src.virus.Virus import Virus


class Game:
    def __init__(self, stores, players, rounds=10):
        self.stores = stores
        self.players = players
        self.rounds = rounds

        self.players_alive = []
        self.players_queue = queue.Queue()

    def add_players(self, players):
        self.players.extend(players)

    def add_stores(self, stores):
        self.stores.extend(stores)

    def run(self):

        if len(self.stores) < 1 or len(self.players) < 1:
            print(colored("Please add more stores or players.", "red"))
            return None

        self.players_alive = self.players.copy()
        round_number = 1

        # print information of round
        self.print_game_state(init=True)

        # prompt to start game
        input(colored("Press enter to begin:", "blue"))

        while round_number <= self.rounds:
            # check for players alive
            if len(self.players_alive) == 0:
                break

            # insert alive players into turn queue
            for player in self.players_alive:
                self.players_queue.put(player)

            print("==================== ROUND ", round_number, " ====================")

            # let each player make a move
            for i in range(len(self.players_alive)):
                player = self.players_queue.get()
                print("Player " + player.name + "'s turn:")

                # process current player
                player.process()
                if not player.is_alive():
                    # remove player from alive list
                    self.players_alive.remove(player)

                    text = "    Player " + player.name + " have died, score: " + str(player.score)
                    print(colored(text, 'red'))
                    continue

                # choose move text
                choose_move_text = ""
                j = 0
                for j in range(len(self.stores)):
                    choose_move_text += "(" + str(j) + ") "
                    choose_move_text += self.stores[j].name
                    choose_move_text += ", "
                choose_move_text += " (" + str(j + 1) + ") stay home: "

                # read move and check validity
                move = input(choose_move_text)
                try:
                    move = int(move)
                except ValueError:
                    move = 100  # set default move, stay home

                # process move
                if move >= len(self.stores):
                    print("    Player " + player.name + " choose to stay home")

                elif move >= 0:
                    store = self.stores[move]
                    print("    Player " + player.name + " goes to " + store.name)

                    # get food from store
                    player.add_food(store.get_food())

                    # player might also get viruses from the store
                    for virus in store.get_virus_list():
                        if Chance.get_random(virus.get_current_infection_chance()):
                            # a copy of the virus is transferred to the player
                            new_virus = create_virus_copy(virus)
                            player.add_virus(new_virus)

                    # todo: player might also bring virus to the store
                else:
                    print("invalid move: still stayed home")

                # increment score
                player.score = round_number

            # process the stores virus
            for store in self.stores:
                store.process()

            # print information of round
            self.print_game_state()

            round_number = round_number + 1

            # prompt to start next round
            input(colored("Press enter to start the next round:", "blue"))

        print("==================== GAME OVER ====================")

        for player in self.players:
            print("Player ", player.name, "score: ", player.score)

    def print_game_state(self, init=False):
        if init:
            print("==================== INITIAL GAME STATE ====================")
        else:
            print(colored("Round summary", "blue"))

        # stores
        for store in self.stores:
            print(store.name + ": ")
            if len(store.get_virus_list()) == 0:
                print("    no virus present")
            else:
                for virus in store.get_virus_list():
                    print("    virus: ", virus.name, "--- infection rate: ", virus.get_current_infection_chance())

        # players
        for player in self.players:
            if player.is_alive():
                print("player:", player.name, colored("alive", "cyan"))
                print("    health:", player.health, "food:", player.food)
                if len(player.viruses) == 0:
                    print("    no virus present")
                else:
                    for virus in player.viruses:
                        print("    virus: ", virus.name,
                              colored(("infection rate: " + str(virus.get_current_infection_chance())), "yellow"))

            else:
                print("player:", player.name, colored("dead", "red"))


def create_virus_copy(virus):
    return Virus(
        name=virus.name + "_copy",
        total_length=virus.total_length,
        infection_chance=virus.base_infection_chance,  # high for testing, 0.2
        severe_chance=virus.base_severe_chance,  # high for testing, 0.2
        damage=virus.damage,  # high for testing
        decay_rate=virus.decay_rate,
    )
