import tkinter as tk
from time import sleep
from Game import Game
from PySnake import PySnake

class Platform(tk.Tk):

    def __init__(self, icon = None):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.game = None
        self.quit = False
        self.create_menu()
        self.binds()
        self.refresh()

    def create_menu(self):
        self.selection  = tk.StringVar(self)
        self.menu_frame = tk.Frame(self) 
        self.menu       = tk.OptionMenu(self.menu_frame, self.selection, "PySnake", "Tetris", "Pacman")
        self.fill       = tk.Frame(self, width = 505, height = 505)
        self.fill_label = tk.Label(self, text = "Select a game.", font = ("Lucida Console", 10))
        self.selection.trace("w", self.handle_option)
        self.fill.grid(      row = 1, column = 0, sticky = tk.W + tk.E)
        self.fill_label.grid(row = 2, column = 0, sticky = tk.W + tk.E)
        self.menu_frame.grid(row = 0, column = 0, sticky = tk.W + tk.E)
        self.menu.pack(side = "left")

    def handle_option(self, *args, **kwargs):
        title = self.selection.get()
        if self.game != None:
            self.game.quit()
            self.game = None
        if title == "PySnake":
            self.game = PySnake(self)
        elif title == "Tetris":
            self.game = Game(self, "Tetris", 501, 501)
        elif title == "Pacman":
            self.game = Game(self, "Pacman", 501, 501)
        else:
            return
        self.game.grid(row = 1, column = 0, columnspan = 2)

    def binds(self):
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind('<Escape>', self.handle_esc)

    def on_closing(self):
        if self.game != None:
            self.game.quit()
            self.game = None
        self.quit = True

    def handle_esc(self, event):
        if self.game == None:
            self.on_closing()

    def refresh(self):
        self.selection.set("Menu")
        self.title("Games")
        self.game = None
        self.quit = False

    def mainloop(self):
        while not self.quit:
            self.update()
            self.update_idletasks()
            if self.game:
                self.game.update()
                if self.game.done():
                    self.refresh()

if __name__ == "__main__":
    Platform().mainloop()
