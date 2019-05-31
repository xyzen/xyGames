import tkinter as tk
from struct import pack, unpack
from time import time, gmtime, strftime

NEW_GAME  = 0
ACTIVE    = 1
PAUSED    = 2
GAME_OVER = 3
GAME_WON  = 4
QUIT      = 5

class Game(tk.Frame):

    def __init__(self, master, title, width, height, *args, **kwargs):
        self.master     = master
        self.title      = title
        self.state      = NEW_GAME
        self.highscore  = 0
        self.score      = 0
        self.start_time = None
        self.master.title(self.title)
        self.create_buttons()
        self.create_field(width, height, *args, **kwargs)
        self.create_display()
        self.read_highscore()

    def update(self):
        pass

    def handle_choice(self, *args, **kwargs):
        pass

    def grid(self, *args, **kwargs):
        self.grid_args   = args
        self.grid_kwargs = kwargs
        self.field.grid(*args, **kwargs)

    def destroy(self):
        self.disp_frame.destroy()
        self.field.destroy()
        self.pause_button.destroy()
        self.restart_button.destroy()
        self.quit_button.destroy()
        self.ai_menu.destroy()

    def toggle_pause(self):
        if self.state == ACTIVE:
            self.state = PAUSED
            self.pause_message = self.field.create_text(
                self.field_width//2, self.field_height//2,
                text = "PAUSED",
                fill = "white",
                font = ("Lucida Console", 20, "bold"))
            self.pause_time = time()
        elif self.state == PAUSED:
            self.state = ACTIVE
            self.field.delete(self.pause_message)
            self.start_time += time() - self.pause_time

    def restart(self):
        self.destroy()
        self.__init__(self.master, self.title, 501, 501)
        self.field.grid(*self.grid_args, **self.grid_kwargs)

    def quit(self):
        self.write_highscore()
        self.destroy()
        self.state = QUIT

    def done(self):
        return self.state == QUIT

    def create_buttons(self):
        self.pause_button = tk.Button(  self.master.menu_frame, text = "Pause",   command = self.toggle_pause)
        self.restart_button = tk.Button(self.master.menu_frame, text = "Restart", command = self.restart)
        self.quit_button = tk.Button(   self.master.menu_frame, text = "Quit",    command = self.quit)
        self.ai_choice  = tk.StringVar(self.master.menu_frame)
        self.ai_choice.set("AI Menu")
        self.ai_menu    = tk.OptionMenu(self.master.menu_frame, self.ai_choice, "A* Search", "Q Learning")
        self.ai_choice.trace("w", self.handle_choice)
        self.pause_button.pack(side = "left")
        self.restart_button.pack(side = "left")
        self.quit_button.pack(side = "left")
        self.ai_menu.pack(side = "right")

    def create_field(self, width, height, *args, **kwargs):
        self.field_width  = width
        self.field_height = height
        self.field = tk.Canvas(
            self.master,
            width  = width,
            height = height,
            *args, **kwargs)

    def create_display(self):
        self.disp_frame  = tk.Frame(self.master)
        self.hscore_disp = None
        self.score_disp  = None
        self.time_disp   = None
        self.disp_frame.grid(sticky = tk.W + tk.E, row = 2, column = 0, columnspan = 2)

    def read_highscore(self):
        try:
            with open(self.title + '.dat', 'rb') as hs:
                hs_bytes = hs.read()
            self.highscore = unpack('h', hs_bytes)[0]
        except:
            pass
        self.update_highscore()
        

    def write_highscore(self):
        if self.score <= self.highscore:
            return
        self.highscore = self.score
        hs_bytes = pack('h', self.highscore)
        try:
            with open(self.title + '.dat', 'wb') as hs:
                hs.write(hs_bytes)
        except:
            pass

    def update_highscore(self):
        self.write_highscore()
        if self.hscore_disp != None:
            self.hscore_disp.pack_forget()
        if self.highscore <= 0:
            temp = "             "
        else:
            temp = "High Score: " + str(self.highscore)
        self.hscore_disp = tk.Label(self.disp_frame, text = temp, font = ("Lucida Console", 10))
        self.hscore_disp.pack(side = tk.LEFT, anchor = tk.W)

    def update_score(self, points = 1):
        if self.score_disp != None:
            self.score += points
            self.score_disp.pack_forget()
        self.score_disp = tk.Label(self.disp_frame, text = "Score: " + str(self.score), font = ("Lucida Console", 10))
        self.score_disp.pack(side = tk.LEFT, fill = tk.X, expand = True, anchor = tk.CENTER)

    def update_time(self):
        if self.start_time == None:
            self.start_time = time()
        else:
            self.time_disp.pack_forget()
        elapsed = strftime("%H:%M:%S", gmtime(time() - self.start_time))
        diff = len("High Score: " + str(self.highscore)) - 8
        self.time_disp = tk.Label(self.disp_frame, text = (" " * diff) + elapsed, font = ("Lucida Console", 10))
        self.time_disp.pack(side = tk.LEFT, anchor = tk.E)

    def game_over(self):
        string = ""
        if self.state == GAME_WON:
            string += "CONGRATULATIONS!\nYou won!\n"
        old = int(self.highscore)
        if self.score > old:
            self.update_highscore()
            self.update_score(0)
            string += "NEW HIGH SCORE!\nOld "
        elif self.state != GAME_WON:
            string += "GAME OVER\n"
        string += "High Score: {}\nScore: {}".format(old, self.score)
        self.field.create_text(
            self.field_width//2, self.field_height//2,
            text    = string,
            fill    = "white",
            font    = ("Lucida Console", 20, "bold"),
            justify = tk.CENTER)
        self.state = GAME_OVER
