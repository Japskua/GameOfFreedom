'''
Created on Feb 4, 2012

@author: japskua
'''

import struct

MAX_BUFFER_SIZE = 128

class Messager(object):
    '''
    classdocs
    '''


    def __init__(self, verbose):
        '''
        Constructor
        '''
        self.verbose = verbose
        
        # The packer class
        #self.struct = struct.Struct()
        
    def CreateJoinMessage(self):
        """
        Creates the Join message
        @return: The message in correct format, that can be
                 sent to the server
        @rtype: String
        """
        # Define the message ID
        messageId = 1
        message = struct.pack("!i", messageId)
        
        # Add the proper line endings
        #message = AddCarriageLineReturnFeed(message)
        
        # Return the correct message
        return message
    
    def CreateQuitMessage(self):
        """
        Creates the QUIT message
        @return: The message in correct format
        @rtype: String
        """
        # First, define the message ID
        messageId = 40
        message = struct.pack("!i", messageId)
        
        # Add the proper line endings
        #message = AddCarriageLineReturnFeed(message)
        
        # Return the correct message
        return message
    
    def CreatePlaceMessage(self, marker, position):
        """
        Creates the PLACE message
        @param marker: The marker the player is using (X/O)
        @type marker: Character
        @param position: The number of the board on where to place the marker
        @type position: Integer
        @return: The message in correct format
        @rtype: String
        """
        

        # First, define the message ID
        messageId = 11
        
        # Then, pack the values to the message
        #message = struct.pack("hh1", id, marker, position)
        message = struct.pack('!ici', messageId, marker, position)
        
        # Finish of with nice CLRF ;-)
        #message = AddCarriageLineReturnFeed(message)
        
        # Return the completed message
        return message