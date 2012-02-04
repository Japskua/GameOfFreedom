'''
Created on Feb 4, 2012

@author: japskua
'''

from helpers import AddCarriageLineReturnFeed

class Messager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    def CreateJoinMessage(self):
        """
        Creates the Join message
        @return: The message in correct format, that can be
                 sent to the server
        @rtype: String
        """
        # Define the message ID
        message = "1"
        
        # Add the proper line endings
        message = AddCarriageLineReturnFeed(message)
        
        # Return the correct message
        return message
    
    def CreateQuitMessage(self):
        """
        Creates the QUIT message
        @return: The message in correct format
        @rtype: String
        """
        # First, define the message ID
        message = "40"
        
        # Add the proper line endings
        message = AddCarriageLineReturnFeed(message)
        
        # Return the correct message
        return message