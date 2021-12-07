import pygame #allows use of pygame
import time #allows use of time

whitewins=0 #sets how many wins each side has at start
pinkwins=0

kingmode=input("do you want to play normal or king only mode? normal or king ")
while kingmode != "normal" and kingmode != "king":
    kingmode=input("do you want to play normal or king only mode? normal or king ")

gamecount=int(input("How many games would you like to play? ")) #finds out how many games to run
colors= input("Would you like classic colored checkers or synthwave checkers? synth or classic? ") #finds what theme player wants
if colors == "synth": #theme 1
    PINK = (255, 110, 180)
    WHITE = (255, 255, 255)
    AQUA = (0, 255, 255)
    DPINK = (255, 20, 147)
elif colors == "classic": #theme 2
    PINK = (255, 0, 0)
    WHITE = (0, 0, 0)
    AQUA = (50, 50, 50)
    DPINK = (0, 0, 255)
else:
    print("sorry that isn't valid") #quits program if they give an invalid answer
    quit()

GOLD = pygame.transform.scale(pygame.image.load("gold.png"), (44, 25)) #loads image that will be on piece when it becomes a king

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        if game.winner() != None:
            print(game.winner())
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #ends the game
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN: #selects a piece where mouse clicks
                pos = pygame.mouse.get_pos()
                row, col = mouse_location(pos)
                game.select(row, col)
        game.update()

class Board:
    def __init__(self):
        z=ROWS/2
        z=int(z)
        x=z*amount
        x=int(x)
        self.board = []
        self.pink_left = self.white_left = x #how many pieces that have to be killed on one side for a winner
        self.pink_kings = self.white_kings = 0
        self.create_board()
    def squares(self, win):
        win.fill(AQUA) #background
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, PINK, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) #draws the checkerboard
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == ROWS - 1 or row == 0: #if a piece makes it to the opposite end it becomes a king
            piece.make_king()
            if piece.color == WHITE:#which side gets a king
                self.white_kings += 1
            else:
                self.pink_kings += 1
    def get_piece(self, row, col):
        return self.board[row][col]
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < amount:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > ROWS - amount - 1:
                        self.board[row].append(Piece(row, col, PINK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    def draw(self, win):
        global kingmode
        if kingmode == "king":
            self.squares(win)
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.board[row][col]
                    if piece != 0:
                        piece.draw(win)
                        piece.make_king()
        elif kingmode == "normal":
            self.squares(win)
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.board[row][col]
                    if piece != 0:
                        piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == PINK:
                    self.pink_left -= 1
                else:
                    self.white_left -= 1
    def winner(self):
        global whitewins
        global pinkwins
        if self.pink_left <= 0: #whole section prints how many wins each side has at the end of each game and returns who won last game
            whitewins=whitewins+1
            whitewins=str(whitewins)
            pinkwins=str(pinkwins)
            if colors == "synth":
                print("white has " + whitewins +" wins and pink has " + pinkwins + " wins")
                whitewins = int(whitewins)
                pinkwins = int(pinkwins)
                return ("White wins!")
            elif colors == "classic":
                print("black has " + whitewins + " wins and red has " + pinkwins + " wins")
                whitewins = int(whitewins)
                pinkwins = int(pinkwins)
                return("Black wins!")
        elif self.white_left <= 0:
            pinkwins=pinkwins+1
            whitewins = str(whitewins)
            pinkwins = str(pinkwins)
            if colors == "synth":
                print("white has " + whitewins + " wins and pink has " + pinkwins + " wins")
                whitewins = int(whitewins)
                pinkwins = int(pinkwins)
                return ("Pink wins!")
            elif colors == "classic":
                print("black has " + whitewins + " wins and red has " + pinkwins + " wins")
                whitewins = int(whitewins)
                pinkwins = int(pinkwins)
                return("Red wins!")
        else:
            pass

    def moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        if piece.color == PINK or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        return moves
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = PINK
        self.valid_moves = {}
    def winner(self):
        return self.board.winner()
    def reset(self):
        self._init()
    def select(self, row, col):
        if self.selected:
            result = self.move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.moves(piece)
            return True
        return False
    def move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        return True
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, DPINK,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == PINK:
            self.turn = WHITE
        else:
            self.turn = PINK

class Piece:
    PADDING = 10
    OUTLINE = 0
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
    def make_king(self):
        self.king = True
    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, PINK, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(GOLD, (self.x - GOLD.get_width() // 2, self.y - GOLD.get_height() // 2))
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
    def rep(self):
        return str(self.color)

FPS = 60 #sets fps as it could fluctate based on how good of a computer runs it

WIN = pygame.display.set_mode((800, 800)) #sets screen size
pygame.display.set_caption("Customizable Checkers") #sets name at top of window

def mouse_location(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

for i in range(gamecount):
    ROWS= int(input("how many rows do you want?")) #asks how big of a board to make
    COLS= ROWS
    SQUARE_SIZE = 800//ROWS #how big the squares will be

    amount=int(input("how many rows of pieces would you like?")) #asks how many of rows to load
    while amount >= ROWS/2:
        amount = int(input("how many rows of pieces would you like?")) #asks again if original answer doesn't work
    main()