from random import randint

VALID_SQUARES = ["1", "2", "3", "4", "5", "6", "7", "8", "9"] #valid input for board
WINNING_COMBOS = {"c1": ["1","2","3"], 
				  "c2":["4","5", "6"], 
				  "c3":["7","8","9"], 
				  "c4":["1", "4", "7"], 
				  "c5":["2", "5", "8"], 
				  "c6":["3", "6", "9"], 
				  "c7":["1", "5", "9"], 
				  "c8":["3", "5", "7"]
				  } #combinations of locations that create a line on the board

CORNER_SQUARES = ["1", "3", "7", "9"]
CENTRE_SQUARE = "5"

def printBoard(board):
	for line in board:
		print line

#checks if square is empty
def isSquareFree(square, playedSquares):
	if square in playedSquares:
		return False
	else:
		return True

#checks if there is a combo where all numbers are satisfied (indicating someone has won)
def isWinner(playedSquares):
	matchingCombos = checkCombos(playedSquares)
	if 3 in matchingCombos.values():
		return True
	return False

#checks current played squares against winning combinations and counts matching numbers for each combination
def checkCombos(playedSquares):
	matchingCombos = {}
	for index, combo in WINNING_COMBOS.items():
		matches = 0
		for number in combo:
			if number in playedSquares:
				matches += 1
		
		matchingCombos[index] = matches
	return matchingCombos

# checks if someone will win on their next turn and returns square needed to win
def checkNextTurn(playedSquares, allPlayedSquares):
	matchingCombos = checkCombos(playedSquares) 
	for comboIndex, matches in matchingCombos.items():
		if matches == 2:
			for number in WINNING_COMBOS[comboIndex]:
				if isSquareFree(number, allPlayedSquares):
					return number
	return None

#counts number of spaces occupied by Xs and Os
def isBoardFull(board):
	occupiedSquares = 0
	for line in board:
		occupiedSquares += line.count("X")
		occupiedSquares += line.count("O")
	
	if occupiedSquares == 9: #all squares are occupied
		return True
	else:
		return False

#Adds X or O to the board at the specified square and adds to the appropriate collection of played squares
def placeOnBoard(board, square, letter):
	board = [line.replace(square, letter) for line in board]
	if letter == "X":
		playerSquares.append(square)
	else:
		computerSquares.append(square)
	allPlayedSquares.append(square)
	return board

#Gets input from user and checks if input is a valid square, then adds it to board
def playerMove(board):
	square = raw_input("Enter the number of the square where you would like to place your piece: ")
	
	while not isSquareFree(square, playerSquares) or square not in VALID_SQUARES:
		square = raw_input("Invalid square! Pick another square: ")
	
	return placeOnBoard(board, square, "X")

#Calculates the computer's next move
def computerMove(board, playerSquares, computerSquares, allPlayedSquares):
	print "Computer move:"
	#check if computer can win next turn and play that square
	squareToPlay = checkNextTurn(computerSquares, allPlayedSquares)
	if squareToPlay is not None:
		return placeOnBoard(board, squareToPlay, "O")

	#check if player will win next turn and stop them
	squareToPlay = checkNextTurn(playerSquares, allPlayedSquares)
	if squareToPlay is not None:
		return placeOnBoard(board, squareToPlay, "O")
	
	#take one of the corner squares if still available
	for corner in CORNER_SQUARES: 
		if isSquareFree(corner, allPlayedSquares):
			return placeOnBoard(board, corner, "O")
	
	#take middle square if still available, if not, pick a random spot
	if isSquareFree(CENTRE_SQUARE, allPlayedSquares):
		return placeOnBoard(board, CENTRE_SQUARE, "O")
	else:
		openSquares = [x for x in VALID_SQUARES if x not in allPlayedSquares]
		maxIndex = len(openSquares) - 1
		return placeOnBoard(board, openSquares[randint(0,maxIndex)], "O")


if __name__ == '__main__':
	playerSquares = []
	computerSquares = []
	allPlayedSquares = []
	board = ["1 | 2 | 3", 
			"----------", 
			"4 | 5 | 6",
			"----------",
			"7 | 8 | 9"]
	raw_input("Welcome to Tic Tac Toe! Are you ready to play? Press [enter] to get started.")
	printBoard(board)
	
	#Player and computer can continue taking turns as long as neither of them have won and the board is not full yet
	while not (isWinner(playerSquares) or isWinner(computerSquares) or isBoardFull(board)):
		board = playerMove(board)
		printBoard(board) 
		if isBoardFull(board):
			break
		board = computerMove(board, playerSquares, computerSquares, allPlayedSquares)
		printBoard(board)
	
	if isWinner(playerSquares):
		print "Congratulations! You've won!"
	elif isWinner(computerSquares):
		print "Oh no! You lost!"
	else:
		print "Oh no! The board is full!"
	
