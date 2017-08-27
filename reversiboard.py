import pygame
from pygame import Rect

# Directions to try from current square.
def buildDirections():
    offsets = [-1, 0, 1]
    directions = []

    for i in offsets:
        for j in offsets:
            if i != 0 or j != 0:
                directions.append((i, j))

    return directions

DIRECTIONS = buildDirections()

class ReversiBoard(object):

    # 2-D matrix of squares, set to size x size in constructor.
    squares = []

    def __init__(self, size, sides):
        self.size = size
        self.sides = sides

        # Fill out entire board with None.
        for row in range(self.size):
            self.squares.append([])

            for col in range(self.size):
                self.squares[row].append(None)

        # Set middle four squares to alternating colors.
        midLow = self.size // 2 - 1
        midHigh = self.size // 2
        self.squares[midLow][midLow] = self.sides[0]
        self.squares[midHigh][midHigh] = self.sides[0]
        self.squares[midLow][midHigh] = self.sides[1]
        self.squares[midHigh][midLow] = self.sides[1]


    # Determine the squares flipped by a particular move.
    # Does not actually apply the move in question.
    def resultOfMove(self, move, player, opponent):
        self.squares[move[0]][move[1]] = player
        # List of squares that this move flips
        allFlipped = []

        # Check all directions for flipped squares.
        for dir in DIRECTIONS:
            # Go until we hit the edge of the board or our own color.
            s = (move[0] + dir[0], move[1] + dir[1])
            while self.inBounds(s) and self.squares[s[0]][s[1]] == opponent:
                s = (s[0] + dir[0], s[1] + dir[1])

            # If we hit our own color, flip all squares between original move
            # the space we hit with our own color.
            if self.inBounds(s) and self.squares[s[0]][s[1]] == player:
                flipped = (move[0] + dir[0], move[1] + dir[1])
                while self.squares[flipped[0]][flipped[1]] == opponent:
                    allFlipped.append(flipped)
                    flipped = (flipped[0] + dir[0], flipped[1] + dir[1])

        return allFlipped

    def inBounds(self, square):
        return square[0] in range(self.size) and square[0] in range(self.size)

    def apply(self, squares, player):
        if squares is not None:
            for square in squares:
                self.squares[square[0]][square[1]] = player

    def copy(self, other):
        other = ReversiBoard(self.size, self.sides)
        for row in range(self.size):
            for col in range(self.size):
                self.squares[row][col] = other[row][col]
        return other

# Fraction of space that gaps take up, vs. total board.
GAP_FRACTION = 1 / 8
# Fraction of window's smallest dimension that board takes up.
BOARD_IN_WINDOW_FRACTION = 0.9
# How much of each square a piece takes up.
PIECE_DIAMETER_FRACTION = 0.8

class ReversiBoardDrawer(object):

    def __init__(self, board, surface, windowWidth, windowHeight,
                 bgColor, boardBgColor, squareColor, sides, colors):

        self.board = board
        self.surface = surface
        self.bgColor = bgColor
        self.boardBgColor = boardBgColor
        self.squareColor = squareColor
        self.sides = sides
        self.colors = colors

        boardDim = int(min(windowWidth, windowHeight) * BOARD_IN_WINDOW_FRACTION)

        self.gapSize = int((boardDim * GAP_FRACTION) / (board.size + 1))
        self.squareSize = int((boardDim * (1.0 - GAP_FRACTION)) / board.size)
        self.pieceRadius = int(self.squareSize * PIECE_DIAMETER_FRACTION / 2)

        self.boardSize = self.squareSize * board.size + self.gapSize * (board.size + 1)
        self.top = (windowHeight - boardDim) // 2
        self.left = (windowWidth - boardDim) // 2

    def drawBoard(self):
        self.drawBackground()
        self.drawLines()
        self.fillSquares()
        pygame.display.update()

    def drawBackground(self):
        self.surface.fill(self.bgColor)

        rect = Rect(self.left, self.top, self.boardSize, self.boardSize)
        pygame.draw.rect(self.surface, self.squareColor, rect)

    def drawLines(self):
        inc = self.gapSize + self.squareSize

        for i in range(self.board.size + 1):
            vrect = Rect(self.left + i * inc,
                         self.top,
                         self.gapSize,
                         self.boardSize)
            pygame.draw.rect(self.surface, self.boardBgColor, vrect)
            hrect = Rect(self.left,
                         self.top + i * inc,
                         self.boardSize,
                         self.gapSize)
            pygame.draw.rect(self.surface, self.boardBgColor, hrect)

    def fillSquares(self):
        inc = self.gapSize + self.squareSize

        for row in range(self.board.size):
            for col in range(self.board.size):
                print("checking " + str(row) + ", " + str(col))
                if self.board.squares[row][col] is not None:
                    cx = self.left + col * inc + self.gapSize + (self.squareSize // 2)
                    cy = self.top + row * inc + self.gapSize + (self.squareSize // 2)
                    color = self.colors[self.board.squares[row][col]]
                    pygame.draw.circle(self.surface, color, (cx, cy), self.pieceRadius)

    def drawMove(self, move, player):
        self.drawBoard()
        pygame.display.update()

    def pointToSquare(self, pos):
        posInBoard = (pos[0] - self.left, pos[1] - self.top)

        if self.outOfBounds(posInBoard[0]) or self.outOfBounds(posInBoard[1]):
            return None

        totalSquareSize = self.squareSize + self.gapSize

        whereInSquare = (posInBoard[0] % totalSquareSize, posInBoard[1] % totalSquareSize)
        if (whereInSquare[0] < self.gapSize or whereInSquare[1] < self.gapSize):
            return None

        squarePicked = (posInBoard[1] // totalSquareSize, posInBoard[0] // totalSquareSize)
        print("picked " + str(squarePicked[0]) + ", " + str(squarePicked[1]))
        return squarePicked

    def outOfBounds(self, coord):
        return coord < 0 or coord >= self.boardSize