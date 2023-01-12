###
#UALG 2022/23
#Metaheuristic
#a78830 - Helder Oliveira
#a78279 - Luciano Neves

import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

#Board alocation pieces
opponentsBoard = np.zeros((10, 10))
#Aircraft Carrier - 5
opponentsBoard[4:9, 8] = 1
#Battleship - 4
opponentsBoard[9, 2:6] = 1
#Submarine - 3
opponentsBoard[2:5, 1] = 1
#Cruiser - 3
opponentsBoard[6, 4:7] = 1
#Destroyer - 2
opponentsBoard[1, 5:7] = 1

visitedBoard = np.zeros((10, 10))
boardProbabilities = np.zeros((10, 10))

#generate board game
#def generatePlot(board):
def generatePlot(board, counter):
    name = "plot" + str(counter)
    cmap = 'cividis'
    
    #l, =plt.plot([],[],'k-')
    #fig = plt.figure()

    ax = sns.heatmap(board, linewidth=0.5, cmap=cmap, cbar=False)
    plt.legend([], [], frameon=False)
    ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    ax.set_yticklabels(['10', '9', '8', '7', '6', '5', '4', '3', '2', '1'])
    rcParams['figure.figsize'] = 11, 11
    plt.savefig(name)
    #plt.show()

    #MAKE A INTERECTIVE GIF 
    # metada = dict(title='Battleship-Metaheurist_UALG_2022', artist='group7')
    # writer = PillowWriter(fps=5, metadata=metada)

    # xList=[]
    # yList=[]

    # with writer.saving(fig, "Battleship-Metaheurist_UALG_2022.gif", 100):
    #     for xVal in np.linspace(-5,5,1):
    #         xList.append(xVal)
    #         yList.append(xVal)

    #         l.set_data(xList,yList)
    #         writer.grab_frame()

#Posistions board
listOfAvailableMoves = []
for i in range(0,10):
    for j in range (0,10):
        listOfAvailableMoves.append(str(i)+str(j))
#print(listOfAvailableMoves)   

#Random guess board
def randomGuessBot(opponentsBoard, visitedBoard, counter, successfulHits, listOfAvailableMoves):
    if successfulHits >= 17:
        print("number of turns:" + str(counter),
              "number of hits:" + str(successfulHits))
        generatePlot(visitedBoard, counter)
        return (True)
    
    random_num = random.choice(listOfAvailableMoves)
    listOfAvailableMoves.remove(random_num)
    row = int(random_num[0])
    col = int(random_num[1])
    generatePlot(visitedBoard, counter)

    if opponentsBoard[row, col] == 1:
        successfulHits += 1
        visitedBoard[row, col] = 1
    else:
        visitedBoard[row, col] = 2
    
    randomGuessBot(opponentsBoard, visitedBoard, counter +
                   1, successfulHits, listOfAvailableMoves)

#randomGuessBot(opponentsBoard, visitedBoard, 0 , 0 , listOfAvailableMoves)

def generateRandomMove(listOfAvailableMoves):
    return (random.choice(listOfAvailableMoves))


def generateNextMove(boardProbabilities):
    return (np.unravel_index(boardProbabilities.argmax(), boardProbabilities.shape))

# #Agressive scan for every boats neighbourhood
def createProbabilities(boardProbabilities, lastHit):
    if lastHit[0] >= 0 and lastHit[0] <= 9 and lastHit[1]+1 >= 0 and lastHit[1]+1 <= 9:
        if boardProbabilities[lastHit[0], lastHit[1]+1] == 0:
            boardProbabilities[lastHit[0], lastHit[1]+1] = 0.25

    if lastHit[0] >= 0 and lastHit[0] <= 9 and lastHit[1]-1 >= 0 and lastHit[1]-1 <= 9:
        if boardProbabilities[lastHit[0], lastHit[1]-1] == 0:
            boardProbabilities[lastHit[0], lastHit[1]-1] = 0.25

    if lastHit[0]+1 >= 0 and lastHit[0]+1 <= 9 and lastHit[1] >= 0 and lastHit[1] <= 9:
        if boardProbabilities[lastHit[0]+1, lastHit[1]] == 0:
            boardProbabilities[lastHit[0]+1, lastHit[1]] = 0.25

    if lastHit[0]-1 > 0 and lastHit[0] <= 9 and lastHit[1]-1 >= 0 and lastHit[1] <= 9:
        if boardProbabilities[lastHit[0]-1, lastHit[1]] == 0:
            boardProbabilities[lastHit[0]-1, lastHit[1]] = 0.25

    return (boardProbabilities)


def randomProbability(opponentsBoard, turnCounter, succesfulHits, listOfAvailableMoves, boardProbabilities, lastHit, missed, visitedBoard):
    if succesfulHits >= 17 or turnCounter >= 100:
        print("Number of turns: " + str(turnCounter),
              "Hits:" + str(succesfulHits))
        generatePlot(visitedBoard, turnCounter+100)
        return

    if (lastHit == -1):  # last hit was miss && don't know have a place to check, so we take random guess
        #print("random", turnCounter)
        random_num = generateRandomMove(listOfAvailableMoves)
        listOfAvailableMoves.remove(random_num)
        row = int(random_num[0])
        col = int(random_num[1])
        generatePlot(visitedBoard, turnCounter+100)

        if opponentsBoard[row, col] == 1:
            succesfulHits += 1
            lastHit = [row, col]
            visitedBoard[row, col] = 1
            boardProbabilities[row, col] = -10  # random hit
            visitedBoard[row, col] = 1
            createProbabilities(boardProbabilities, lastHit)

        else:
            boardProbabilities[row, col] = -1  # miss
            visitedBoard[row, col] = 2

    else:
        nextHit = generateNextMove(boardProbabilities)
        position = str(nextHit[0])+str(nextHit[1])
        if position in listOfAvailableMoves:  # should always be true
            listOfAvailableMoves.remove(position)
            row = nextHit[0]
            col = nextHit[1]
            generatePlot(visitedBoard, turnCounter+100)
            if boardProbabilities[row, col] == 0:  # out of guesses
                lastHit = -1

            boardProbabilities[row, col] = -1

            if opponentsBoard[row, col] == 1:
                succesfulHits += 1
                lastHit = [row, col]
                visitedBoard[row, col] = 1
                boardProbabilities[row, col] = -100  # rated move hit
                visitedBoard[row, col] = 1
                missed = 0
            else:
                missed = 1
                visitedBoard[row, col] = 2

    randomProbability(opponentsBoard, turnCounter+1, succesfulHits,
                           listOfAvailableMoves, boardProbabilities, lastHit, missed, visitedBoard)


randomProbability(opponentsBoard, 0, 0, listOfAvailableMoves,
                       boardProbabilities, -1, 0, visitedBoard)

# def generateRandomMove(listOfAvailableMoves):
#     return (random.choice(listOfAvailableMoves))


#print(opponentsBoard)

#generate board with pieces inside
#generatePlot(opponentsBoard)

