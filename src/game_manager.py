from Game import Game
from location.Location import Location
from player.Player import Player
from virus.Virus import Virus

NUMBER_OF_ROUNDS = 20
PLAYER_HEALTH = 100  # starting hp
PLAYER_MAX_FOOD = 8  # most food a player can hold
PLAYER_FOOD = 5  # starting food
PLAYER_HUNGER = 25  # player will lose this number of hp if they have no food for 1 round


def create_player(name):
    return Player(
        name=name,
        health=PLAYER_HEALTH,
        max_food=PLAYER_MAX_FOOD,
        food=PLAYER_FOOD,
        hunger=PLAYER_HUNGER
    )


# http://www.acphd.org/communicable-disease/communicable-diseases.aspx used as a reference
def create_virus_copy(virus):
    return Virus(
        name=virus.name + "_copy",
        total_length=virus.total_length,
        infection_chance=virus.base_infection_chance,  # high for testing, 0.2
        severe_chance=virus.base_severe_chance,  # high for testing, 0.2
        damage=virus.damage,  # high for testing
        decay_rate=virus.decay_rate,
    )


def create_influenza_virus():
    return Virus(
        name="Influenza",
        total_length=12,
        infection_chance=0.3,
        severe_chance=0.2,
        damage=15,
        decay_rate=0.9,
    )


def create_mrsa_virus():
    return Virus(
        name="MERS",  # Methicillin-resistant S. Aureus
        total_length=8,
        infection_chance=0.6,
        severe_chance=0.4,
        damage=40,
        decay_rate=0.5,
    )


def create_covid_19_virus():
    return Virus(
        name="covid-19",
        total_length=7,
        infection_chance=0.4,  # high for testing, 0.2
        severe_chance=0.5,  # high for testing, 0.2
        damage=100,  # high for testing
        decay_rate=0.6,
    )


def create_store_walmart(food):
    return Location(
        name="Walmart",
        food=food
    )


def create_tim_hortons(food):
    return Location(
        name="Tim Horton's",
        food=food
    )


def create_game(stores, players, number_of_rounds=10):
    return Game(
        stores=stores,
        players=players,
        rounds=number_of_rounds
    )


def create_test_game():
    game = create_game([], [], NUMBER_OF_ROUNDS)

    # create players
    p1 = create_player("p1")
    p2 = create_player("p2")
    p3 = create_player("p3")
    players = [p1, p2, p3]

    # create viruses
    covid_19 = create_covid_19_virus()
    influenza = create_influenza_virus()
    mrsa = create_mrsa_virus()

    # create stores
    walmart = create_store_walmart(5)
    tim_hortons = create_tim_hortons(1)
    stores = [walmart, tim_hortons]

    # add viruses to stores
    walmart.add_virus(covid_19)
    walmart.add_virus(influenza)
    tim_hortons.add_virus(mrsa)

    # add components to game
    game.add_players(players)
    game.add_stores(stores)

    return game
