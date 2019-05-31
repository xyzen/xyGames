SNAKE = 0
APPLE = 1

class Tile():

    def __init__(self, x, y, master = None, tag = SNAKE, size = 20):
        self.x = x
        self.y = y
        if master != None:
            self.master = master
            self.draw(tag, size)

    def __eq__(self, other):
        if other == None:
            return self.x == None and self.y == None
        return self.x == other.x and self.y == other.y

    def coords(self, size):
        x1 = self.x * size + 2
        y1 = self.y * size + 2
        x2 = x1 + size
        y2 = y1 + size
        return x1, y1, x2, y2

    def draw(self, tag, size):
        if   tag == SNAKE:
            self.repr = self.master.create_rectangle(*self.coords(size), fill = "#000fff000")
        elif tag == APPLE:
            self.repr = self.master.create_oval(*self.coords(size), fill = "red")

    def darken(self):
        self.master.itemconfig(self.repr, fill = "green")

    def erase(self):
        self.master.delete(self.repr)

    def __hash__(self):
        tpl = tuple([self.x, self.y])
        return tpl.__hash__()