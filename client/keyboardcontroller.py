'''
Created on Feb 4, 2012

@author: japskua
'''

import sys

class KeyboardController(object):
    '''
    classdocs
    '''
    command_join = "/join"
    command_quit = "/quit"
    command_place = "/place"

    def __init__(self):
        '''
        Constructor
        '''
        
    def ReadInput(self):
        """
        Acts according the input
        """
        # Read the input from the command line
        input = sys.stdin.readline()
        
        # Get the command from the input line
        self.GetCommand(input)
        
    def GetCommand(self, input):
        """
        Gets the command from the user input
        """
        # If the command is join
        if input.startswith(KeyboardController.command_join):
            # Send the join message to the server
            print input
            
        # If the command is quit
        elif input.startswith(KeyboardController.command_quit):
            # Send the quit message to the server
            print input
            
        # If the command is place
        elif input.startswith(KeyboardController.command_place):
            # Get the placement number
            try:
                placement = int(input.split(" ")[1])
                # Send the placement message to the server
                print input
            except:
                print "Please, provide a correct number"
        
        # Otherwise, inform of the available commands    
        else:
            print "The available commands are /join /quit /place <position>"

        