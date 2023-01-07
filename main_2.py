###
#UALG 2022/23
#Metaheuristic
#a78830 - Helder Oliveira
#a78279 - Luciano Neves

import csv

turnCountArray = []

#Function to plot results
def plotResults(file):
   
    Interations = []
    Shots = []
    
    with open(file,'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
            Interations.append((row[0]))
            Shots.append(float(row[1]))
    
    plt.scatter(Interations, Shots, color = 'g',s = 100)
    plt.xticks(rotation = 25)
    plt.xlabel('Interations')
    plt.ylabel('Shots')
    plt.title('Optimized algorithm shot attempt report', fontsize = 20)

    mean = np.mean(Shots)
    plt.plot([0, len(Shots)], [mean, mean])
    plt.legend([mean])
    plt.show()

#Simulation Benchmark machine
for h in range(1, 11):    
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from matplotlib import colors
    from matplotlib import rcParams
    from matplotlib.animation import PillowWriter
    import time 
    from itertools import chain
    import random

    #Generate the plot
    def generatePlot(board_with_probabilities, turn_counter):
       
        name = "plot" + str(turn_counter)
        cmap = 'cividis'

        #Map to represnt probabilities
        cmap = colors.ListedColormap(['slateblue','red','lightgreen']) if turn_counter >= 100 else 'magma'    

        ax = sns.heatmap(board_with_probabilities , linewidth = 0.5 , cmap = cmap, cbar=False)
        #plt.legend([],[], frameon=False)
        ax.set_xticklabels(['1','2','3','4','5','6','7','8', '9', '10'])
        ax.set_yticklabels(['10','9','8','7','6','5','4','3', '2', '1'])
        rcParams['figure.figsize'] = 11,11
        #plt.imshow(board_with_probabilities, cmap='plasma', linewidth = 0.5)
        plt.savefig(name)

        """
        #MAKE A INTERECTIVE GIF 
        metada = dict(title='Battleship-Metaheurist_UALG_2022', artist='group7')
        writer = PillowWriter(fps=15, metadata=metada)

        xList=[]
        yList=[]

        with writer.saving(fig, "Battleship-Metaheurist_UALG_2022.gif", 100):
            for xVal in np.linspace(-5,5,1):
                xList.append(xVal)
                yList.append(xVal)

                l.set_data(xList,yList)
                writer.grab_frame()
        """

    #Generates ships fixed/randomly inside the board
    def generateRandomBoard():
        opponents_board = np.full((10, 10), 0)
        """
        #Fixed ships on board
        #
        #Aircraft Carrier - 5
        opponents_board[4:9, 8] = 1
        #Battleship - 4
        opponents_board[9, 2:6] = 1
        #Submarine - 3
        opponents_board[2:5, 1] = 1
        #Cruiser - 3
        opponents_board[6, 4:7] = 1
        #Destroyer - 2
        opponents_board[1, 5:7] = 1

        """
        #Randomly
        #
        ships = [5,4,3,3,2]

        for length_of_the_ship in ships:
            placed = False
            while placed == False:
                col_or_row = random.randint(0,1)
                
                # row
                if col_or_row == 1:  
                    empty_slot_counter = 0              
                    random_row = random.randint(0,9)
                    random_col = random.randint(0,9-length_of_the_ship)

                    for i in range(0,length_of_the_ship):
                        if opponents_board[random_row,random_col+i] == 0:
                            empty_slot_counter += 1

                    if empty_slot_counter == length_of_the_ship:
                        for i in range(0,length_of_the_ship):
                            opponents_board[random_row,random_col+i] = 1
                        placed = True

                # col
                if col_or_row == 0:  
                    empty_slot_counter = 0              
                    random_col = random.randint(0,9)
                    random_row = random.randint(0,9-length_of_the_ship)

                    for i in range(0,length_of_the_ship):
                        if opponents_board[random_row+i,random_col] == 0:
                            empty_slot_counter += 1

                    if empty_slot_counter == length_of_the_ship:
                        for i in range(0,length_of_the_ship):
                            opponents_board[random_row+i,random_col] = 1
                        placed = True
       
        return(opponents_board)

    #Find possible locations summarize by the ship size
    def possibibleLocationsProbability(board_with_hits, board_with_misses, length_of_the_ship):
        list_of_probabilities = []
        
        # Check all rows for possible locations
        for row in range(0,10):
            for col in range(0,11-length_of_the_ship):
                positions_to_consider = range(col, col+length_of_the_ship)
                # State where hits happened
                positions_with_hits = []
                empty_slot_counter = 0

                # Check if the elements of a list all correspond to 0s, and if they do create a matrix where that segment has a certain probabiliity
                for element in positions_to_consider:
                    if board_with_misses[row,element] == 0:
                        if board_with_hits[row, element] == 1:
                            positions_with_hits.append(element)    
                        empty_slot_counter += 1

                # Check if the number of continious empty slots corresponds to the length of the ship   
                if empty_slot_counter == length_of_the_ship:
                    new_state = np.full((10, 10), 0.0)
                    if_there_is_hit = 4*len(positions_with_hits) if len(positions_with_hits) else 1
                    for element in positions_to_consider:
                        if element in positions_with_hits:
                            new_state[row, element] = 0
                        else:    
                            new_state[row,element] = float(length_of_the_ship) * if_there_is_hit
                    list_of_probabilities.append(new_state)

        # Check all cols for possible locations
        for col in range(0,10):
            for row in range(0,11-length_of_the_ship):
                positions_to_consider = range(row, row+length_of_the_ship)
                positions_with_hits = []
                empty_slot_counter = 0

                # Check if the elements of a list all correspond to 0s, and if they do create a matrix where that segment has a certain probabiliity
                for element in positions_to_consider:
                    if board_with_misses[element,col] == 0:
                        if board_with_hits[element,col] == 1:
                            positions_with_hits.append(element)
                        empty_slot_counter += 1

                # Check if the number of continious empty slots corresponds to the length of the ship   
                if empty_slot_counter == length_of_the_ship:
                    if_there_is_hit = 4 if len(positions_with_hits) else 1

                    new_state = np.full((10, 10), 0.0)
                    for element in positions_to_consider:
                        if element in positions_with_hits:
                            new_state[element,col] = 0
                        else:    
                            new_state[element,col] = float(length_of_the_ship) * if_there_is_hit
                    list_of_probabilities.append(new_state)


        final_matrix = np.full((10, 10), 0)
        for curr_matrix in list_of_probabilities:
            final_matrix = np.add(final_matrix, curr_matrix)

        return(final_matrix)

    #Generate probabilties for all ships
    def generateProbabilitiesForAllShips(board_with_hits, board_with_misses):
        final = np.full((10, 10), 0)
        ships = [5,4,3,3,2]
        for i in ships:
            probabilites = possibibleLocationsProbability(board_with_hits, board_with_misses, i)
            final = np.add(final, probabilites)
        return(final)

    #Next move function
    def generateNextMove(board_with_probabilities):
        return(np.unravel_index(board_with_probabilities.argmax(), board_with_probabilities.shape))

    #Array occurrence count function
    def count_occurrences(matrix, element):
        # Converts the matrix to a list of numbers
        numbers = [num for row in matrix for num in row]
        # Count how many times the element appears in the list
        return numbers.count(element)

    #Function add values to List
    def addCountValuesList(turn_counter,h):
        
        R1 = []
        R2 = []

        if turnCountArray == []:
                R1.append(h)
                R2.append(turn_counter)
                results = list(chain(R1,R2))
                turnCountArray.append(results)
                #print('Your array is empty')
                print(turnCountArray)
                print("mean of arr : ", np.mean(R2))
        else:
            R1.append(h)
            R2.append(turn_counter)
            results = list(chain(R1,R2))
            turnCountArray.append(results)
            #print('Your array is not empty')
            print(turnCountArray)
            print("mean of arr : ", np.mean(R2))

    #Function bot
    def bot (opponents_board, board_with_hits, board_with_misses, turn_counter, successful_hits):
        
        misses = count_occurrences(board_with_misses,2)

        if successful_hits >= 17 or turn_counter>=100:
            #generatePlot((board_with_hits+board_with_misses), turn_counter + 100)
            print("In Simulation number ",h,
                "\nnumber of turns:" + str(turn_counter),
                "\nnumber of hits:" + str(successful_hits),
                "\nnumber of misses:" + str(misses))

                   
            addCountValuesList(turn_counter,h)
                    
            return (turn_counter) 

        board_with_probabilities = generateProbabilitiesForAllShips(board_with_hits, board_with_misses)
        nextHit = generateNextMove(board_with_probabilities)
        row = nextHit[0]
        col = nextHit[1]

        #TODO: ===> Enable / Disable to plot a game board ilustration  <===
        #
        #generatePlot(board_with_probabilities, turn_counter)
        #generatePlot((board_with_hits+board_with_misses), turn_counter + 100)

        if opponents_board[row,col] == 1:    
            successful_hits += 1
            board_with_hits[row,col] = 1
            board_with_probabilities[row,col] = 0 

        else:
            board_with_misses[row,col] = 2

        return (bot (opponents_board, board_with_hits, board_with_misses, turn_counter+1, successful_hits))
   
    final_sum = 0
    opponents_board = generateRandomBoard()
    board_with_probabilities = np.zeros((10,10))
    board_with_hits = np.zeros((10,10))
    board_with_misses = np.zeros((10,10))
    final_sum += bot(opponents_board, board_with_hits, board_with_misses, 0, 0)
       
time.sleep(0) # Pauses every time loop ends by 0.5 seconds 
np.savetxt('result.csv',turnCountArray , delimiter = ',',fmt='%i') #Save results to CSV file
plotResults('result.csv')


