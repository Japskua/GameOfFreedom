'''
Created on Feb 5, 2012

@author: japskua
'''

class GameBoard(object):
    '''
    The GameBoard object handles all the board-related functions
    and stores the board pieces and state. This class is used 
    both by the server (to handle all the logic) and the clients
    (to store the board state)
    '''

    MARKER_X = "X"
    MARKER_O = "O"
    MARKER_EMPTY = "-"

    def __init__(self, verbose):
        '''
        Create the board
        '''
        
        self.verbose = verbose
        self.board = []
        
    def CreateBoard(self):
        """
        Creates a new empty board
        """
        
        # First, initialize to be empty
        if self.verbose:
            print "Creating the initial empty board"
            
        # Loop through the whole list
        for position in range(0, 100):
            # And set it to be empty marker
            self.board.append(GameBoard.MARKER_EMPTY)
            
        if self.verbose:
            print "Board initialized"
            
            
    def DisplayBoard(self):
        """
        Displays the complete game board
        """
        
        if self.verbose:
            print "Displaying the board"
            print "Board size is:", len(self.board)
            
        # Loop through the whole list
        for position in range(0,100):
            if (position == 0):
                print "|", self.board[position], 
                if self.verbose:
                    print position,
            elif (position == 99):
                print "|", self.board[position], 
                if self.verbose:
                    print position, 
                print "|"
            # If the value is not divisible by 9
            elif (position % 9) == 0:
                print "|", self.board[position], 
                if self.verbose:
                    print position, 
                print "|"
            else:
                # Display the markers
                print "|", self.board[position], 
                if self.verbose:
                    print position,
            
        #print self.board[99]

            

        
        
        