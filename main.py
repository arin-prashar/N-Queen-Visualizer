import pygame
import asyncio

WIDTH = 600
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
# ROW determines the number of queens on the board, if you are making queens more than 5, it is suggested that you change the time to 20-50ms on line 201

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("N-Queen Visualizer")
pygame.init()

# take row as input using pygame textbox
ROW = 8


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.total_rows = total_rows
        self.width = width
        self.color = WHITE
        self.neighbors = []
        self.queen = pygame.image.load("queen.png")
        self.queen = pygame.transform.scale(self.queen, (width, width))

    def __str__(self):
        return str(self.row) + "," + str(self.col)

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_checking(self):
        return self.color == BLUE

    def is_checking_for(self):
        return self.color == YELLOW

    def is_reset(self):
        return self.color == WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_checking(self):
        self.color = BLUE

    def make_reset(self):
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        # draw the image
        if self.color == BLACK:
            win.blit(self.queen, (self.x, self.y))

    def __lt__(self, other):
        return False


def algorithm(grid):
    sol = solveNQUtil(lambda: draw(WIN, grid, ROW, WIDTH), grid, 0)
    if not sol:
        print("No Solution")
        return False
    else:
        print("Solution Found")
        return True


def isSafe(draw, grid, row, col):
    temp = grid[row][col].color
    grid[row][col].make_open()
    draw()
    # Check this row on left side
    for i in range(col):
        if grid[row][i].is_barrier():
            grid[row][i].make_closed()
            draw()
            grid[row][i].make_barrier()
            draw()
            for j in range(col):
                if j == i:
                    continue
                grid[row][j].make_reset()
                # draw()
            grid[row][col].make_reset()
            return False
        if not grid[row][i].is_open():
            grid[row][i].make_checking()
            draw()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].is_checking():
                grid[i][j].make_reset()
                # draw()

    # Check upper diagonal on left side
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if grid[i][j].is_barrier():
            grid[i][j].make_closed()
            draw()
            grid[i][j].make_barrier()
            draw()
            for i2, j2 in zip(range(row, -1, -1), range(col, -1, -1)):
                if i2 == i and j2 == j:
                    continue
                grid[i2][j2].make_reset()
                # draw()
            grid[row][col].make_reset()
            return False
        if not grid[i][j].is_open():
            grid[i][j].make_checking()
            draw()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].is_checking():
                grid[i][j].make_reset()
                # draw()

    # Check lower diagonal on left side
    for i, j in zip(range(row, ROW, 1), range(col, -1, -1)):
        if grid[i][j].is_barrier():
            grid[i][j].make_closed()
            draw()
            grid[i][j].make_barrier()
            draw()
            for i2, j2 in zip(range(row, ROW, 1), range(col, -1, -1)):
                if i2 == i and j2 == j:
                    continue
                grid[i2][j2].make_reset()
                # draw()
            grid[row][col].make_reset()
            return False
        if not grid[i][j].is_open():
            grid[i][j].make_checking()
            draw()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].is_checking():
                grid[i][j].make_reset()
                # draw()
    grid[row][col].color = temp
    return True


def solveNQUtil(draw, grid, col):

    # base case: If all queens are placed
    # then return true
    if col >= ROW:
        return True

    # Consider this column and try placing
    # this queen in all rows one by one
    for i in range(ROW):

        if isSafe(draw, grid, i, col):

            # Place this queen in board[i][col]
            grid[i][col].make_barrier()
            draw()
            # recur to place rest of the queens
            if solveNQUtil(draw, grid, col + 1) == True:
                return True

            # If placing queen in board[i][col
            # doesn't lead to a solution, then
            # queen from board[i][col]
            grid[i][col].make_reset()
            draw()

    # if the queen can not be placed in any row in
    # this column col then return false
    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.flip()
    pygame.time.wait(50)


async def main(win, width):
    asyncio.sleep(0)
    grid = make_grid(ROW, width)
    run = True
    started = False

    while run:
        draw(win, grid, ROW, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            started = True
            algorithm(grid)
            await asyncio.sleep(0)
        await asyncio.sleep(0)
    pygame.quit()


asyncio.run(main(WIN, WIDTH))
