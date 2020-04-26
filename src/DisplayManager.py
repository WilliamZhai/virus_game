import time
import tkinter as tk
import threading
from functools import partial

from termcolor import colored
import game_manager as GM
from Game import GameState

MAIN_CANVAS_WIDTH = 800
MAIN_CANVAS_HEIGHT = 400
TOOL_BAR_CANVAS_WIDTH = 800
TOOL_BAR_CANVAS_HEIGHT = 50

color1 = '#66e0ff'
color2 = '#ff8533'
color3 = '#ff9933'
color_alive = '#00e600'
color_dead = '#ff1a1a'



class DisplayManager:
    global game_thread

    def __init__(self, root):
        self.root = root
        self.game = None

        self.tool_bar_canvas = None

        self.main_canvas = None
        self.title = None

        self.options_canvas = None

        self.stores_display = []
        self.players_display = []

    def set_game_move(self, move):
        self.game.set_move(move)
        time.sleep(0.2)  # sleeps until
        self.update_game_state()

    def end_game_thread(self):
        #self.game.end_game()
        self.main_canvas.delete('all')
        self.main_canvas.pack_forget()
        self.create_main_display(self.root)
        return

    def create_game_thread(self):
        self.game = GM.create_test_game()
        game_thread = threading.Thread(target=self.game.run, daemon=True)
        game_thread.daemon = True
        game_thread.start()
        self.update_game_state()

    def update_game_state(self):
        # update main display
        self.title.destroy()

        if self.game.get_game_state() == GameState.FINISHED:

            # todo: display score and go back to main menu

            self.end_game_thread()
            return

        # stores
        stores_label = tk.Label(self.main_canvas, text='STORES', bg=color2)
        stores_label.place(x=0, y=0, relwidth=1, height=20)

        number_of_stores = len(self.game.stores)
        stores_x = MAIN_CANVAS_WIDTH / number_of_stores
        stores_height = 0.3

        for i in range(len(self.game.stores)):
            store = self.game.stores[i]

            text_display = tk.Text(self.main_canvas, bd=4)
            text_display.insert(tk.INSERT, '                    ' + store.name + '\n')
            text_display.insert(tk.INSERT, 'Viruses present: \n')

            scrollbar = tk.Scrollbar(text_display)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            scrollbar.config(command=text_display.yview)

            for j in range(len(store.viruses)):
                virus = store.viruses[j]

                text_display.insert(tk.INSERT, str(j + 1) + ') ' + virus.name + '\n')
                text_display.insert(tk.INSERT, '    Infection chance: ' +
                                    str(virus.get_current_infection_chance()) + '\n')

                start = str(2 + ((j + 1) * 2)) + '.22'
                end = str(2 + ((j + 1) * 2)) + '.25'
                text_display.tag_add('rate', start, end)
                text_display.tag_config('rate', background=color3)

            text_display.place(x=i * stores_x, y=20, relheight=stores_height, relwidth=1 / number_of_stores)

        # display players
        players_label = tk.Label(self.main_canvas, text='PLAYERS', bg=color2)
        players_label.place(x=0, y=140, relwidth=1, height=20)

        number_of_players = len(self.game.players)
        players_x = MAIN_CANVAS_WIDTH / number_of_players
        players_height = 0.3

        for i in range(len(self.game.players)):
            player = self.game.players[i]
            if player.is_alive():
                player_color = color_alive
            else:
                player_color = color_dead

            player_frame = tk.LabelFrame(self.main_canvas, text=player.name)
            player_frame.place(x=i * players_x + 2, y=0.3 * MAIN_CANVAS_HEIGHT + 40, relheight=players_height,
                               relwidth=1 / number_of_players)

            text_display = tk.Text(player_frame, bg=player_color)
            text_display.insert(tk.INSERT, 'Health: ' + str(player.health) + '\n')
            text_display.insert(tk.INSERT, 'Food: ' + str(player.food) + '\n')
            text_display.insert(tk.INSERT, 'Viruses: ' + '\n')
            for j in range(len(player.viruses)):
                virus = player.viruses[j]

                text_display.insert(tk.INSERT, str(j + 1) + ') ' + virus.name + '\n')
                text_display.insert(tk.INSERT, '    Infection chance: ' +
                                    str(virus.get_current_infection_chance()) + '\n')

                start = str(3 + ((j + 1) * 2)) + '.22'
                end = str(3 + ((j + 1) * 2)) + '.25'
                text_display.tag_add('rate', start, end)
                text_display.tag_config('rate', background=color3)

            text_display.pack()

        self.update_option_canvas()

    def update_option_canvas(self):
        # player
        current_player = self.game.turn

        controller_label = tk.Label(self.main_canvas, text='CONTROLLER', bg=color2)
        controller_label.place(x=0, y=280, relwidth=1, height=20)

        instruction = 'Round ' + str(self.game.current_round) + ' Player ' + current_player.name + '\'s turn'

        instruction_label = tk.Label(self.main_canvas, text=instruction)
        instruction_label.place(x=0, y=300, relwidth=1, height=20)

        # player controller options
        number_of_stores = len(self.game.stores)
        options_x = MAIN_CANVAS_WIDTH / (number_of_stores + 1)
        options_height = 0.2
        options_label = []
        for i in range(len(self.game.stores)):
            txt = 'go to ' + self.game.stores[i].name
            options_label.append(
                tk.Button(self.main_canvas, text=txt, bg=color1, command=partial(self.set_game_move, i)))
            options_label[i].place(x=i * options_x, y=320, relheight=options_height,
                                   relwidth=1 / (number_of_stores + 1))

        txt = 'stay home '
        i = number_of_stores
        options_label.append(tk.Button(self.main_canvas, text=txt, bg=color1, command=partial(self.set_game_move, i)))
        options_label[i].place(x=i * options_x, y=320, relheight=options_height, relwidth=1 / (number_of_stores + 1))

    def create_tool_bar(self, parent):
        self.tool_bar_canvas = tk.Canvas(parent, width=TOOL_BAR_CANVAS_WIDTH, height=TOOL_BAR_CANVAS_HEIGHT,
                                         bg='#666666')
        self.tool_bar_canvas.pack(side='bottom')

        start_button = tk.Button(self.tool_bar_canvas, text='Start', command=self.create_game_thread, bd=4)
        start_button.place(x=0, y=0, relheight=0.8, relwidth=1 / 3, rely=0.1, relx=0.008)

        quit_button = tk.Button(self.tool_bar_canvas, text='Quit', command=self.end_game_thread, bd=4)
        quit_button.place(x=TOOL_BAR_CANVAS_WIDTH / 3, y=0, relheight=0.8, relwidth=1 / 3, rely=0.1, relx=0.008)

        submit_button = tk.Button(self.tool_bar_canvas, text='Submit', command=None, bd=4)  # todo: add
        submit_button.place(x=TOOL_BAR_CANVAS_WIDTH / 3 * 2, y=0, relheight=0.8, relwidth=(1 / 3) - 0.01, rely=0.1,
                            relx=0.008)

    def create_main_display(self, parent):
        self.main_canvas = tk.Canvas(parent, width=MAIN_CANVAS_WIDTH, height=MAIN_CANVAS_HEIGHT, bg=color1)
        self.main_canvas.pack()

        self.title = tk.Label(self.main_canvas, text='Virus Game')
        self.title.config(font=("Courier", 44, "bold"))
        self.title.place(x=0, y=0, relheight=0.9, relwidth=0.9, rely=0.05, relx=0.05)
