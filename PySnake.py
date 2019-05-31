from collections import deque
from random import sample
from time import sleep
from Tile import Tile
from Game import *

UP    = 'w'
DOWN  = 's'
LEFT  = 'a'
RIGHT = 'd'

backwards = { UP:DOWN, DOWN:UP, LEFT:RIGHT, RIGHT:LEFT }

class SnakeState():

    def __init__(self, snake, apple, cells, state, path, depth):
        self.snake = deque([(cell.x, cell.y) for cell in snake])
        self.head  = self.snake[0]
        self.tail  = self.snake[-1]
        self.apple = (apple.x, apple.y)
        self.cells = set((cell.x, cell.y) for cell in cells)
        self.state = state
        self.depth = depth

    def update_head(self):
        self.snake.appendleft(self.head)
        self.cells.discard(self.head)

    def update_tail(self):
        self.snake.pop()
        if self.head != self.tail:
            self.cells.add(self.tail)
        self.tail  = self.snake[-1]

    def move_head(self, direction):
        if self.direction   == UP:
            self.head.y -= 1
        elif self.direction == DOWN:
            self.head.y += 1
        elif self.direction == LEFT:
            self.head.x -= 1
        elif self.direction == RIGHT:
            self.head.x += 1
        else:
            pass

    def next_state(self, direction):
        new_state = SnakeState(self.snake, self.apple, self.cells, self.state, self.path, self.depth).move_head(direction)
        if new_state.head == new_state.apple: 
            new_state.update_head()
            new_state.apple = None
            if not len(new_state.cells):
                new_state.state = GAME_WON
        elif new_state.head in new_state.cells \
            or new_state.head == new_state.tail and (len(new_state.snake) > 1):
            new_state.update_head()
            new_state.update_tail()
        elif new_state.head in new_state.snake:
            new_state.update_head()
            new_state.update_tail()
            new_state.state = GAME_OVER
        else:
            new_state.state = GAME_OVER
        return new_state

    def expand(self):
        next_states = []
        for direction in backwards:
            new_state = next_state(direction)
            if new_state.state != GAME_OVER:
                next_states.append()
        return tuple(next_states)

class PySnake(Game):
    
    def __init__(self, master, *args, **kwargs):
        Game.__init__(self, master, "PySnake", 501, 501, bg = "black")
        self.field.bind_all('<KeyPress>', self.handle_key)
        self.create_cells(20)
        self.create_snake()
        self.place_apple()

    def update(self):
        if self.state == ACTIVE:
            self.next_frame()
            self.update_time()
            sleep(0.15)
        return self.done()

    def handle_key(self, event):
        sym = event.keysym.lower()
        if sym in backwards:
            if self.state == NEW_GAME:
                self.direction = sym
                self.next_key  = deque([sym])
                self.update_score()
                self.update_time()
                self.state = ACTIVE
            else:
                self.next_key.append(sym)
        elif sym == 'space':
            self.next_key.clear()
            if self.state in (ACTIVE, PAUSED):
                self.toggle_pause()
            elif self.state == GAME_OVER:
                self.restart()
        elif sym == 'escape':
            if self.state != ACTIVE:
                self.quit()
            else:
                self.toggle_pause()
        elif sym == 'r':
            if self.state != ACTIVE:
                self.restart()

    def create_cells(self, cell_size):
        self.grid_width  = self.field_width//cell_size
        self.grid_height = self.field_height//cell_size
        self.cells = set([])
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                self.cells.add(Tile(row, col))

    def create_snake(self):
        self.head  = Tile(self.grid_height//2, self.grid_width//2)
        self.tail  = Tile(self.head.x, self.head.y)
        self.snake = deque([Tile(self.head.x, self.head.y, self.field)])
        self.cells.discard(self.head)

    def place_apple(self):
        if self.state != NEW_GAME:
            self.apple.erase()
        random     = sample(self.cells, 1)[0]
        self.apple = Tile(random.x, random.y, self.field, tag = 1)

    def update_head(self):
        self.snake[0].darken()
        self.snake.appendleft(Tile(self.head.x, self.head.y, self.field))
        self.cells.discard(self.head)
    
    def update_tail(self):
        self.snake.pop().erase()
        if self.head != self.tail:
            self.cells.add(Tile(self.tail.x, self.tail.y))
        new_tail  = self.snake[-1]
        self.tail = Tile(new_tail.x, new_tail.y)

    def move_head(self):
        while len(self.next_key) and self.next_key[0] == backwards[self.direction]:
                self.next_key.popleft()
        if len(self.next_key) and self.next_key[0] != backwards[self.direction]:
            self.direction = self.next_key.popleft()
        if self.direction   == UP:
            self.head.y -= 1
        elif self.direction == DOWN:
            self.head.y += 1
        elif self.direction == LEFT:
            self.head.x -= 1
        elif self.direction == RIGHT:
            self.head.x += 1
        else:
            pass

    def next_frame(self):
        self.move_head()
        if self.head == self.apple:
            self.update_head()
            self.place_apple()
            self.update_score()
            if not len(self.cells):
                self.state = GAME_WON
                self.game_over()
        elif self.head in self.cells \
            or (len(self.snake) > 1) and (self.head == self.tail):
            self.update_head()
            self.update_tail()
        elif self.head in self.snake:
            self.update_head()
            self.update_tail()
            self.game_over()
        else:
            self.game_over()
            