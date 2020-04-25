from src import game_manager as GM
from src.DisplayManager import DisplayManager
import tkinter as tk


if __name__ == '__main__':
    """
    We start this game with 3 players, 2 stores, and 3 viruses
    """

    # main root
    root = tk.Tk(screenName=None, baseName=None, className='Tk', useTk=1)
    root.title('Game')

    dm = DisplayManager(root)
    dm.create_tool_bar(root)
    dm.create_main_display(root)

    # start application
    root.mainloop()

    exit(0)
