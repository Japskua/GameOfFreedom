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
            

    def TryPlaceMarker(self, position, marker):
        """
        This function is used to try to place a marker
        at the given position.
        @param position: The position at the game board
        @type position: Integer
        @param marker: The marker to place at the given position
        @type marker: String ('X' or 'O')
        @return: True if the placement was succesfull
                 False if not
        @rtype: Boolean
        """
        
        if self.verbose:
            print "Trying to place marker", marker, "at position", position
            
        # Check if the given marker is correct
        if (marker != GameBoard.MARKER_O) and (marker != GameBoard.MARKER_X):
            if self.verbose:
                print "The marker is neither 'X' nor 'O'"
            # If not, return false
            return False
            
        # Check if the place is empty
        if self.board[position] != GameBoard.MARKER_EMPTY:
            if self.verbose:
                print "The placement position is not empty!"
            # The place is not free, thus return false
            return False
        
        # Otherwise, make the position to be the given one
        self.board[position] = marker
        
        if self.verbose:
            print "Placed the", marker, "successfully to", position
        
        # And return true as a mark of success
        return True

    def UpdateBoard(self, position, marker):
        """
        Updates the board to be the new defined board
        """
        
        # Set the position to be the given marker
        self.board[position] = marker
        
    
    def GetBoard(self):
        """
        Returns the whole board for sending
        """
        return self.board
        