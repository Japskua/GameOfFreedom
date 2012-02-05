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

    MARKER_X = 'X'
    MARKER_O = 'O'
    MARKER_EMPTY = '-'

    def __init__(self, verbose):
        '''
        Create the board
        '''
        
        self.verbose = verbose
        self.board = []
        
        self._lastPlacement = None
        self._availablePositions = []
        
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
            
    def GetLastPlacement(self):
        """
        Gets the last placement so that the next player
        can be informed of the possible placement
        """
        return self._lastPlacement
            
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
            elif self.CheckIfRightCorner(position) == True:
                print "|", self.board[position], 
                if self.verbose:
                    print position, 
                print "|"
            else:
                # Display the markers
                print "|", self.board[position], 
                if self.verbose:
                    print position,
            
    def CalculateScore(self):
        """
        Calculates the game scores from the board
        """
        scorePlayer1 = 0
        scorePlayer2 = 0
        
        
        return scorePlayer1, scorePlayer2
    
    def GetNextPossiblePlacement(self):
        """
        Gets the next possible placements that 
        then can be sent to the next player
        to inform of his/her possible movements
        """
        position = self.GetLastPlacement()    
        listPlaces = []
        
        if self.verbose:
            print "Getting the next possible placement"
            print "Previous placement was", position
            
        # If the last placement was None, then retun 
        # the empty listPlaces
        if position == None:
            return listPlaces
        
        
        
        # Get the 3-NN Tiles
        listAbove = self.Get3Above(position)
        listSides = self.Get2Sides(position)
        listBelow = self.Get3Below(position)
        
        if self.verbose:
            print "The sizes of the list are the following"
            print "Above:", len(listAbove)
            print "Sides:", len(listSides)
            print "Below:", len(listBelow)
            
        # Then, throw them into one list
        # Checking if the values are okay on the go
        
        # Check, if the list is not empty
        if len(listAbove) > 0:
            for value in listAbove:
                # Check if the marker is empty
                if self.board[value] == GameBoard.MARKER_EMPTY:
                    listPlaces.append(value)
            
        # Check the list size is not 0
        if len(listSides) > 0:
            for value in listSides:
                # Check if the marker is empty
                if self.board[value] == GameBoard.MARKER_EMPTY:
                    listPlaces.append(value)
            
        # Check that the list is bigger than 0
        if len(listBelow) > 0:
            for value in listBelow:
                # Check if the marker is empty
                if self.board[value] == GameBoard.MARKER_EMPTY:
                    listPlaces.append(value)
            
        if self.verbose:
            print "The following places are free"
            for value in listPlaces:
                print value,
            print "\nMaking total of", len(listPlaces), "places"
        
        # Set the available positions checker to be the same as the listPlaces
        self._availablePositions = listPlaces
        
        # Finally, return the list gained
        return self._availablePositions
    
    def Get3Below(self, position):
        """
        Gets the three values below
        """
        
        listPosition = []
        
        # Check if the position is bigger than 90,
        # Because in that case there are no value below
        if position > 89:
            return listPosition
        
        # Get the Left side value
        if self.CheckIfLeftCorner(position) == False:
            listPosition.append(position+9)
            
        # Get the value below
        listPosition.append(position+10)
        
        # Get the right side value
        if self.CheckIfRightCorner(position) == False:
            listPosition.append(position+11)
            
        # Return the list
        return listPosition
                
    def Get2Sides(self, position):
        """
        Gets the 2 values from both of the sides of the placement
        """
        
        listPosition = []
        
        # Check the left corner
        if self.CheckIfLeftCorner(position) == False:
            listPosition.append(position-1)
            
        # Check the right corner
        if self.CheckIfRightCorner(position) == False:
            listPosition.append(position+1)
            
        # Return the list
        return listPosition
        
    def Get3Above(self, position):
        
        listPositions = []
        
        # If the position is less than 10, there are no values above
        if position < 10:
            return listPositions
        
        # Check, if the value is in the left corner
        if self.CheckIfLeftCorner(position) == False:
            listPositions.append(position-11)
              
        # Otherwise, get the value above
        listPositions.append(position-10)
        
        # Check if the value is in the right corner
        if self.CheckIfRightCorner(position) == False:
            listPositions.append(position-9)
        
        # Return the table
        return listPositions
        
    def CheckIfRightCorner(self, position):
        """
        Checks if the given value is in the right side of the table
        """
        listRight = [9, 19, 29, 39, 49, 59, 69, 79, 89, 99]
        
        # If the position is in the list
        if position in (listRight):
            return True
        
        # Otherwise, return False
        return False
        
    def CheckIfLeftCorner(self, position):
        """
        Checks if the given value is in the left side of the table
        """
        
        listLeft = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
        
        # If the position is in the list
        if position in (listLeft):
            return True
        
        # Otherwise return False
        return False
        
        
    def CheckIfInAvailablePositions(self, position):
        """
        Checks if the given position is within the 
        boundaries of the available positions
        """
        
        # Set the found value to be false
        found = False
        
        # If the available positions is empty, return True 
        # Because the placement is then free
        if len(self._availablePositions) == 0:
            return True
        
        # Check, if the given position is within the boudaries of the next free position
        # Loop through the list
        for value in self._availablePositions:
            # If the position is found
            if position == value:
                # Set the found value to true
                found = True
                
        # Return the found value
        return found
        

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
            
        # Check if the value is within the free placement boundaries
        if self.CheckIfInAvailablePositions(position) == False:
            return False
            
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
        
        # Mark the last placement to be the position
        self._lastPlacement = position
        
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
        