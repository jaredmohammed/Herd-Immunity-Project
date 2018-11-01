
# coding: utf-8

# In[4]:


# standard includes
import numpy as np
import numpy.random as rand
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

# Next, import some specific libraries we will use to get the animation to work cleanly
from IPython.display import display, clear_output
import time 

def set_board(board_size=300, vaccine_frac=0.5):
    '''
    Creates the initial game board.

    Inputs:
        board_size: length of one edge of the board
        vaccine_frac: probability that a given cell is a healthy, vaccinated
                       (effectively the healthy, vaccinated cell density)

    Outputs a 2D numpy array with values set to either 0, 1, or 2
        (healthy unvaccinated, healthy vaccinated, or infected)
    '''
    
    # all cells initialized to 'healthy, unvaccinated' (0) by default
    game_board = np.zeros((board_size,board_size),dtype='int64')
    
    # loop over board and roll the dice; if the random number is less
    # than vaccine_frac, make it a healthy, vaccinated cell.
    for i in range(board_size):
        for j in range(board_size):
            if rand.random() <= float(vaccine_frac):
                game_board[i,j] = int(1)
            else:
                game_board[i,j] = int(0)

    # set the middle cells as the board as infected so we can model the spread of disease
    for row in range(147, 152):
        for col in range(147, 152):
            game_board[row, col] = int(2)
    
    return game_board

def plotgrid(myarray):
    # 
    x_range = np.linspace(0, myarray.shape[0], myarray.shape[0]) 
    y_range = np.linspace(0, myarray.shape[0], myarray.shape[0])
    
    # 
    vac_indeces_x = []
    vac_indeces_y = []
    non_vac_indeces_x = []
    non_vac_indeces_y = []
    infected_indeces_x = []
    infected_indeces_y = []
    # 
    for i in range(len(myarray[0])):
        for j in range(len(myarray[0])):
            if myarray[i][j] == 0:
                non_vac_indeces_x.append(int(i))
                non_vac_indeces_y.append(int(j))
            elif myarray[i][j] == 1:
                vac_indeces_x.append(int(i))
                vac_indeces_y.append(int(j))
            elif myarray[i][j] == 2:
                infected_indeces_x.append(int(i))
                infected_indeces_y.append(int(j))
    plt.plot(non_vac_indeces_x,non_vac_indeces_y, 'bs',markersize=1)
    plt.plot(vac_indeces_x,vac_indeces_y, 'gs',markersize=1)
    plt.plot(infected_indeces_x,infected_indeces_y, 'rs',markersize=1)
 
    
    # 
    plt.xlim([-1,len(myarray[0])+1])
    plt.ylim([-1,len(myarray[0])+1]) 

    # 
    plt.tick_params(axis='both', which='both',
                    bottom='off', top='off', left='off', right='off',
                    labelbottom='off', labelleft='off')
    
def advance_board(game_board):
    '''
    Advances the game board using the given rules.
    Input: the initial game board.
    Output: the advanced game board
    '''
    
    # create a new array that's just like the original one, but initially set to all zeros (i.e., totally empty)
    new_board = np.zeros_like(game_board)
    # loop over each cell in the board and decide what to do.
    # Need two loops here, one nested inside the other.
    for i in range(len(game_board)):
        for j in range (len(game_board)):
            i = int(i)
            j = int(j)

            # Now that we're inside the loops we need to apply our rules
            # if the cell was healthy and vaccinated last turn, it's still healthy and vaccinated.
            if int(game_board[i][j]) == 1:
                new_board[i][j] = 1 
            # if it was infected last turn, it's still infected.
            elif int(game_board[i][j]) == 2:
                new_board[i][j] = 2 
    
            # now, if there is a healthy, unvaccinated person in the cell, we have to decide what to do
            elif int(game_board[i][j]) == int(0):
                
                # initially make the cell a healthy, unvaccinated cell in the new board
                new_board[i][j] = 0

                # If one of the neighboring cells was infected last turn, 
                # this cell is now infected
                # make sure you account for whether or not you're on the edge
                if i+1 < len(game_board[0]) and game_board[i+1][j]==2 and rand.random() <= 0.85:
                    new_board[i][j] = 2
                if i > 0 and game_board[i-1][j]==2 and rand.random() <= 0.85:
                    new_board[i][j] = 2
                if j+1 < len(game_board[0]) and game_board[i,j+1]==2 and rand.random() <= 0.85:
                    new_board[i][j] = 2
                if j> 0 and game_board[i][j-1]==2 and rand.random() <= 0.85:
                    new_board[i][j] = 2
                #top right
                if i+1 < len(game_board[0]) and j+1 < len(game_board[0]) and game_board[i+1,j+1]==2 and rand.random() <= 0.85:
                    new_board[i][j] = 2
                #top left
                if i > 0 and j+1 < len(game_board[0]) and game_board[i-1][j+1]==2 and rand.random() <= 0.85:
                    new_board[i][j] = 2
                #bottom left
                if i > 0 and j > 0 and game_board[i-1][j-1]==2 and rand.random() <= 0.85:
                    new_board[i][j] = 2
                #bottom right
                if i+1 < len(game_board[0]) and j > 0 and game_board[i+1][j-1]==2 and rand.random() <= 0.85:
                    new_board[i][j] = 2

    # return the new board
    return new_board

def calc_stats(game_board):
    '''
    Calculates the fraction of cells on the game board that are 
    healthy or infected
    
    Input: a game board
    
    Output: fraction that's infected, fraction that's healthy.
    '''
    
    # count up the fraction that are healthy, unvaccinated
    z=0
    for i in range (0,len(game_board[0])):
        for j in range (0, len(game_board[0])):
            if game_board[i,j] == 0:
                z += 1
    frac_hun = z/game_board.size
            

    # do the same for healthy, vaccinated
    y=0 
    for i in range (0,len(game_board[0])):
        for j in range (0, len(game_board[0])):
            if game_board[i,j] == 1:
                y += 1
    frac_hva = y/game_board.size 
    
    inf = 0
    for i in range (0,len(game_board[0])):
        for j in range (0, len(game_board[0])):
            if game_board[i,j] == 1:
                inf += 1
    frac_inf = inf/game_board.size
    
    # return it!
    return frac_hun, frac_hva

#plots a figure of a specified size
fig = plt.figure(figsize=(10,10))

# sets up an initial array for the gameboard
game_board = set_board(board_size=300, vaccine_frac = 0.5)

#plots gameboard
plotgrid(game_board)


i = 0
while i < 150: #150 person to person interactions / day
    # advances game board
    game_board = advance_board(game_board)
    
    # updates board every .01 time intervals
    plotgrid(game_board)
    time.sleep(0.01)  # 
    clear_output(wait=True)
    display(fig)
    fig.clear()
    print('# of Interactions:', i+1) 
    print("# of Days:        ", (i+1)/150)
    i += 1
    

# finishes plotting
plt.close()

