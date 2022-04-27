from vpython import*
import numpy as np
import random

# list of colors to be randomly chosen for each random block type generated
colors = [ vector(1, 0, 0), vector(0, 1, 0), vector(0, 0, 1), vector(1, 1, 0),
           vector(1, 0, 1), vector(0, 0, 0), vector(1, 1, 1) ]

# class to create blocks
class Block:
    x = 0
    y = 0
    
    # list of Tetrominos and their rotations. Each number represents a cell in an array that represent block type
    blocks = [ [[1, 5, 9, 13], [4, 5, 6, 7]], [[4, 5, 9, 10], [2, 6, 5, 9]],
                [[6, 7, 9, 10], [1, 5, 6, 10]],
                [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
                [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
                [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
                [[1, 2, 5, 6]] ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.blocks) - 1) # randomly select a block type
        self.color = random.randint(1, len(colors) - 1) # randomly select a color
        self.rotation = 0
    
    # returns block type and its current orientation
    def block(self):
        return self.blocks[self.type][self.rotation]
    
    # rotate the block
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.blocks[self.type])

class Tetris:
    score = 0
    state = "start" # signify state of game
    board = [] 
    x = 100 
    y = 60
    zoom = 20
    block = None
    
    # initialize game
    def __init__(self):
        self.board = []
        self.score = 0
        self.state = "start"
        self.height = 20 # height of board
        self.width = 10 # width of board
        
        for i in range(self.height):
            new_line = []
            for j in range(self.width):
                new_line.append(0)
            self.board.append(new_line)
     
    # create new block
    def new_block(self):
        self.block = Block(3, 0)
        
    # check if current block touches another block on the board
    def hit_block(self):
        hit = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.block():
                    if i + self.block.y > self.height - 1 or \
                            j + self.block.x > self.width - 1 or \
                            j + self.block.x < 0 or \
                            self.board[i + self.block.y][j + self.block.x] > 0:
                        hit = True
        return hit
    
    # function to remove line of blocks if valid and increment score
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.board[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.board[i1][j] = self.board[i1 - 1][j]
        self.score += lines ** 2

    # stop block at end of board
    def stop(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.block():
                    self.board[i + self.block.y][j + self.block.x] = self.block.color
        self.break_lines()
        self.new_block()
        if self.hit_block():
            self.state = "end"
            
    ## game controls ##         
    def move_down(self):
        self.block.y += 1
        if self.hit_block():
            self.block.y -= 1
            self.stop()
    
    # move left or right
    def move_side(self, dx):
        old_x = self.block.x
        self.block.x += dx
        if self.hit_block():
            self.block.x = old_x
            
    # rotate block
    def rotate(self):
        old_rotation = self.block.rotation
        self.block.rotate()
        if self.hit_block():
            self.block.rotation = old_rotation

# function to receive keyboard input for controls
def keyInput(evt):
    k = evt.key
    if 'left' in k: game.move_side(-1)
    if 'right' in k: game.move_side(1)
    if 'down' in k: game.move_down()
    if 'up' in k: game.rotate()
    if 'esc' in k: game.state = "end"


# set up game #
scene = canvas()
cellSize = vector(19, 19, .5)
cells = np.zeros((20,10), object)
scene.center = 0.5 * 300 * vector(1,1,-10)
scene.bind('keydown', keyInput)
game = Tetris()

# loop until game is finished
while game.state != "end":
    rate(2)

    # generate new block at start of game or when previous block is stationary
    if game.block is None:
        game.new_block()

    game.move_down()

    # create board with cyan cells
    for i in range(game.height):
        for j in range(game.width):
            # stores visibility of blocks that are stationary at bottom of board
            cells[i,j] = box(pos=vector(game.x + game.zoom * j, game.y + game.zoom * i, 0), color=color.cyan, size=cellSize)
            
            if game.board[i][j] > 0:
                cells[i,j].color = vector(colors[game.board[i][j]])
                
               
    # if there's a block in play on the board
    if game.block is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.block.block():
                    # adjust visibility of block as its moving down board
                    box(pos=vector(game.x + game.zoom * (j + game.block.x), game.y + game.zoom * (i + game.block.y), 0), color=vector(colors[game.block.color]), size=cellSize)

print("Game Over\n")
print("Score: ", game.score)