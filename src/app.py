from src.game_manager import *

NUMBER_OF_ROUNDS = 20

if __name__ == '__main__':
    """
    We start this game with 3 players, 2 stores, and 3 viruses
    """
    game = create_game([], [], NUMBER_OF_ROUNDS)

    # create players
    p1 = create_player("p1")
    p2 = create_player("p2")
    p3 = create_player("p3")
    players = [p1, p2]

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

    # start game
    game.run()
