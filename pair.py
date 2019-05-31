class Tile():

    def __init__(self, master, x, y):
        self.master = master
        self.x = x
        self.y = y

    def __eq__(self, other):
        if other == None:
            return self.x == None and self.y == None
        return self.x == other.x and self.y == other.y

    def to_rect(self, value):
        x1 = self.x * size + 2
        y1 = self.y * size + 2
        x2 = x1 + size
        y2 = y1 + size
        return x1, y1, x2, y2

    def __hash__(self):
        tpl = tuple([self.x, self.y])
        return tpl.__hash__()