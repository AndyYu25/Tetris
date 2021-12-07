from cmu_112_graphics import *
import random
import copy

class Tetris(App):
    def appStarted(self, initialState, isTest=False):
        """Initializes all variables required to play tetris based on
        the input initialState. Default is spawning a random piece on a 
        board with 15 rows and 10 columns"""
        self.board, self.fallingPiece, self.fpr, self.fpc = initialState
        if self.board == None: [['blue' * 10] for r in range(15)]
        self.rows,self.cols,self.margin = len(self.board), len(self.board[0]),25
        #determines the cell size based on the canvas size. may go off canvas
        self.cellSize = min((self.height - 2*self.margin)//self.rows, 
                            (self.width - 2*self.margin)//self.cols)
        self.score, self.gameOver,self.isTest = 0, False, isTest
        #self.placed pieces is a 2D list of coords where a piece has been placed
        self.placedPieces = [[False for c in range(self.cols)] for r in range(self.rows)]
        self.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
        self.tetrisPieceColors = ["red", "yellow", "magenta", "pink", 
                                  "cyan", "green", "orange"]
        self.pieceType = None
        self.pieceColor = None
        #pieceBoard tracks the current falling piece on a separate board
        self.pieceBoard = [['' for c in range(self.cols)] for r in range(self.rows)]
        #generates new falling Piece if no falling piece is given
        if self.fallingPiece == None: self.newFallingPiece() 
        self.setPieceType()
        self.updatePieceBoard()
        self.timer = 0


    def setPieceType(self):
        """determines the type of piece self.fallingPiece is."""
        for piece in self.tetrisPieces:
            if self.fallingPiece == piece():
                self.pieceType = piece
                self.pieceColor = self.tetrisPieceColors[self.tetrisPieces.index(piece)]

    def updatePieceBoard(self):
        """updates Piece Board with the new position of self.fallingPiece"""
        if self.fallingPiece != None:
            #loop iterates through the shape of fallingPiece and colors in 
            #the squares which should be colored in (specified by the True/False
            # 2D List)
            for pieceRow in range(len(self.fallingPiece)):
                for pieceCol in range(len(self.fallingPiece[0])):
                    colOffset = self.fpc + pieceCol
                    rowOffset = self.fpr + pieceRow
                    if colOffset < self.cols:
                        if self.fallingPiece[pieceRow][pieceCol] and \
                            rowOffset < self.rows:
                                self.pieceBoard[rowOffset][colOffset]=self.pieceColor
                        else: self.pieceBoard[rowOffset][colOffset] = ''
            #loop resets colors of pieceBoard to only that of fallingPiece
            for row in range(self.rows):
                for col in range(self.cols):
                    if (row not in range(self.fpr, self.fpr+len(self.fallingPiece)) or \
                        col not in range(self.fpc, self.fpc+len(self.fallingPiece[0]))):
                        self.pieceBoard[row][col] = ''
    def keyPressed(self, event):
        """Takes in key inputs and alters the board accordingly.
        Space moves the piece all the way down the board
        Up rotates the piece counterclockwise
        Down,Left,and Right move the piece in the specified direction
        r restarts the game"""
        if event.key == 'Space':#moves a piece all the way down
            pieceMovedDown = False
            while not pieceMovedDown:
                #if statement checks if the piece can move down further
                if not self.moveFallingPiece(1, 0):
                    self.placeFallingPiece()
                    break
        elif event.key == 'Up':
            self.rotateFallingPiece()
        elif event.key == 'Down':
            if not self.moveFallingPiece(1, 0):
                self.placeFallingPiece()
        elif event.key == 'Left':
            self.moveFallingPiece(0, -1)
        elif event.key == 'Right':
            self.moveFallingPiece(0, 1)
        elif event.key == 'r':
            self.appStarted((None, None, None, None))
    def timerFired(self):
        """increments score by time survived, removes any full rows, and
        moves pieces downwards"""
        self.timer += 1
        speed = 3
        if self.timer % speed == 1:
            if not self.gameOver: self.score += 1
            if not self.moveFallingPiece(1, 0): #automatically moves piece down
                self.placeFallingPiece() 
                self.removeFullRows() #removes any full rows 
            
    def getState(self):
        """returns the current state of the game. For testing purposes."""
        return (self.board, self.fallingPiece, self.fpr,
                self.fpc, self.score, self.gameOver)

    def redrawAll(self, canvas):
        """renders a background, the game board, the score, and a game 
        over screen"""
        #draws background
        canvas.create_rectangle(0, 0, self.width, self.height, fill='orange')
        for row in range(self.rows): #draws the game board
            for col in range(self.cols):
                colX = self.margin+col*self.cellSize
                colY = self.margin+row*self.cellSize
                colX1, colY1 = colX + self.cellSize, colY + self.cellSize
                canvas.create_rectangle(colX,colY, colX1, colY1, 
                                        fill=str(self.board[row][col])) 
                canvas.create_rectangle(colX,colY, colX1, colY1, 
                                        fill=str(self.pieceBoard[row][col]))
        #draws current score
        canvas.create_text(self.width//2, self.margin//2, text=f"Score: {self.score}")
        if self.gameOver: #draws game over banner
            gameOverBannerHeight, gameOverBannerY = 25, self.height//3
            gameOverBannerX = self.margin + self.cols*self.cellSize//2
            canvas.create_rectangle(0, gameOverBannerY-gameOverBannerHeight,
                self.width, gameOverBannerY+gameOverBannerHeight,fill='black')
            canvas.create_text(gameOverBannerX, gameOverBannerY, 
                text=f"Game Over. Your Score was {self.score}",fill='yellow')
    def newFallingPiece(self):
        """creates a random piece on the top of the board"""
        #variables get a random shape and color
        randIndex = random.randint(0, len(self.tetrisPieces) - 1)
        randPiece = self.tetrisPieces[randIndex]()
        randColor = self.tetrisPieceColors[randIndex]
        self.fpc = self.cols//2 - len(randPiece[0])//2 #spawn shape in middle
        self.fpr = 0 # spawn shape up top
        self.fallingPiece = randPiece
        self.setPieceType()
        self.updatePieceBoard()
        #checks the game over condition: if piece cannot be legally spawned
        if not self.fallingPieceIsLegal(): 
            self.gameOver = True
   

    def moveFallingPiece(self, drow, dcol):
        """moves a piece by the specified dRow and dCol. Returns whether or 
        not the move was made successfully"""
        if self.fpr + drow < 0 or self.fpc +dcol < 0:
            return False # if statements check if move is within the grid
        elif self.fpr + len(self.fallingPiece) + drow > len(self.board) or \
            self.fpc + len(self.fallingPiece[0]) + dcol > len(self.board[0]):
            return False
        self.fpr += drow
        self.fpc += dcol
        self.updatePieceBoard()
        if not self.fallingPieceIsLegal():#undo move if move is not legal
            self.fpr -= drow
            self.fpc -= dcol
            self.updatePieceBoard()
            return False
        self.updatePieceBoard()
        return True

    def fallingPieceIsLegal(self):
        """returns if the current position of a falling piece is legal by checking
        whether or not the pieceboard overlaps with the placedPieces or
        board"""
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.pieceBoard[row][col] != '' and \
                    (self.board[row][col] != 'blue' or self.placedPieces[row][col]):
                    return False
        return True
    
    def placeFallingPiece(self):
        """converts a falling piece into a fixed piece on pieceBoard
        and spawns a new piece"""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.pieceBoard[row][col] != '':
                    self.board[row][col] = self.pieceBoard[row][col]
                    self.placedPieces[row][col] = True
        if not self.gameOver: self.newFallingPiece()


    def rotateFallingPiece(self):
        """rotates a falling piece of 90 degrees counterclockwise if 
        method is called"""
        oldPiece = self.fallingPiece #store old values of fallingPiece
        oldDim = (len(self.fallingPiece), len(self.fallingPiece[0]))
        newDim = (oldDim[1], oldDim[0])
        oldPos = (self.fpr, self.fpc)
        oldCenterRow = self.fpr + oldDim[0]//2
        newFPR = oldCenterRow - newDim[0]//2#finds new position of rotated piece
        oldCenterCol = self.fpc + oldDim[1]//2
        newFPC = oldCenterCol - newDim[1]//2
        newPiece = [[None for c in range(newDim[1])] for r in range(newDim[0])]
        for row in range(oldDim[0]):
            for col in range(oldDim[1]): #fills in new piece with transposed values
                newPiece[(oldDim[1]-col-1)][row] = oldPiece[row][col]
        self.fallingPiece = newPiece
        self.fpr, self.fpc = newFPR, newFPC
        if (self.fallingPieceIsLegal() or self.fpr==0) and 0<=self.fpr and \
            self.fpr+newDim[0] < self.rows and \
            0<=self.fpc and self.fpc+newDim[1] < self.cols: 
            self.updatePieceBoard() #checks if rotation is legal
        #undos rotation if rotation is not legal
        else: self.fallingPiece,self.fpr, self.fpc = oldPiece, oldPos[0],oldPos[1]

    def removeFullRows(self):
        """checks if a row is filled with shapes and then removes the row
        and increments score if the row is filled"""
        #stores whether or not a row is filled with tiles
        lineFilled = [True]*self.rows
        for row in range(self.rows):
            for tile in self.board[row]:
                if tile == 'blue':
                    lineFilled[row] = False
        #increments score based on removed rows.
        #Simulateously removed rows are worth more.
        self.score += 5 * (lineFilled.count(True))**2
        #pops any lines filled and adds a blank line to the top of the board
        for row in range(self.rows):
            if lineFilled[row]:
                self.board.pop(row)
                self.pieceBoard.pop(row)
                self.placedPieces.pop(row)
                self.board.insert(0, ['blue']*self.cols)
                self.pieceBoard.insert(0, ['']*self.cols)
                self.placedPieces.insert(0, [False]*self.cols)

####################################
# Running Tetris
####################################

def emptyBoard(rows:int, cols:int) ->list:
    """creates an empty rows x cols 2d list"""
    result = []
    for _ in range(rows):
        result.append(["blue"] * cols)
    return result

def runTetris():
    initialState = (emptyBoard(15, 10), None, None, None)
    Tetris(initialState, width = 450, height = 600)

####################################
# Main
####################################


if __name__ == "__main__":
    runTetris()
