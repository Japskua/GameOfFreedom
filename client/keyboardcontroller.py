'''
Created on Feb 4, 2012

@author: japskua
'''

import sys
from messager import Messager

class KeyboardController(object):
    '''
    classdocs
    '''
    command_join = "/join"
    command_quit = "/quit"
    command_place = "/place"

    def __init__(self, verbose):
        '''
        Constructor
        '''
        self.verbose = verbose
        self.messager = Messager(self.verbose)
        
        
    def ReadInput(self, marker):
        """
        Acts according the input
        """
        # Read the input from the command line
        keyboardInput = sys.stdin.readline()
        
        # Get the command from the input line
        # And return the result
        return self._GetCommand(keyboardInput, marker)
        
    def _GetCommand(self, keyboardInput, marker):
        """
        Gets the command from the user input
        """
        # If the command is join
        if keyboardInput.startswith(KeyboardController.command_join):
            # Create the join message and return it
            return self.messager.CreateJoinMessage()
            
        # If the command is quit
        elif keyboardInput.startswith(KeyboardController.command_quit):
            # Create and return the quit message
            return self.messager.CreateQuitMessage()
            
        # If the command is place
        elif keyboardInput.startswith(KeyboardController.command_place):
            # Get the placement number
            try:
                placement = int(keyboardInput.split(" ")[1])
                
                # If the placement is not between 0 and 99
                if placement < 0 or placement > 99:
                    # Return nothing
                    print "The placement value must be between 0 and 99."
                    return None
                
                # Send the placement message to the server
                return self.messager.CreatePlaceMessage(marker, placement)
            except:
                print "Please, provide a correct number"
                return None
        
        # Otherwise, inform of the available commands    
        else:
            print "The available commands are /join /quit /place <position>"

        # If we are here, something went wrong?, just return none
        return None
        