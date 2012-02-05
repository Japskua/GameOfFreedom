'''
Created on Feb 5, 2012

@author: japskua
'''

import struct

# ENUM

class ErrorEnum(object):
    ERR_PLACEMENT = 1
    ERR_FULL = 2
    ERR_ALREADYJOINED = 3


def SendMessage(socket, ip, port, message):
    """
    Sends the message to the given receiver
    @param socket: The socket from where to send the message
    @type socket: Integer
    @param ip: The IP address of the receiver
    @type ip: String
    @param port: The port where to send the message
    @type port: Integer
    @param message: The packed message to be sent
    @type message: String    
    """
    
    # Send the message
    socket.sendto(message, (ip, port) )
    
    
def CreateAcceptMessage():
    """
    Creates the accept message that can then be
    sent to the client in question
    @return: Returns the message in packed format
             that can then be sent to the client
    @rtype: String
    """

    # Define the message ID
    messageId = 2
    message = struct.pack("!i", messageId)
    
    # Return the correct message
    return message

def CreateErrorMessage(errorType):
    """
    Creates the error message that can be then
    sent to the client
    @type errorType: Integer
    @param errorType: The type of the error in question (errorId)
    @return: Returns the message in packed format
             that can then be sent to the client
    @rtype: String
    """
    
    # Define the message ID
    messageId = 30
    
    # Create the message
    message = struct.pack("!ii", messageId, errorType)
    
    # Return the message
    return message

def CreateGameStartMessage(marker):
    """
    Creates the message signifying the game start
    @param marker: The marker assigned for the player in question
    @type marker: Character (X or O)
    @return: Returns the message in packed format
             that can then be sent to the client
    @rtype: String
    """
    
    # Define the message ID
    messageId = 3
    
    # Create the message
    message = struct.pack("!ic", messageId, marker)
    
    # Return the message
    return message

def CreateTurnMessage(freePlaces, listPlaces):
    """
    Creates the turn message for the player
    @param freePlaces: Amount of free places 
                       NOTE! 0 = Free Placement
    @type freePlaces: Integer
    @param listPlaces: List of the free places on the board
    @type listPlaces: list of Integers
    @return: Returns the message in packed format
             that can then be sent to the client
    @rtype: String
    """
    
    # Define the message ID
    messageId = 10
    
    # Create the message
    message = struct.pack("!ii", messageId, freePlaces)
    
    # If there are more than 0 places free for placement
    if freePlaces > 0:
        # Add the list places to the message
        for n in range(0, freePlaces):
            struct.pack_into("!i", message, 8+n, listPlaces[n])
        
    # Return the message
    return message

def CreateScoreMessage(points1, points2, winner):
    """
    Creates the score message to be sent to both of the players
    @param points1: The amount of points gained by the
                    player with X marker
    @type points1: Integer
    @param points2: The amount of points gained by the
                    player with O marker
    @type points2: Integer
    @param winner: The marker of the winning player
    @type winner: Character (either 'x' or 'o')
    @return: Returns the message in packed format
             that can then be sent to the client
    @rtype: String
    """
    
    # Define the message ID
    messageId = 20
    
    # Create the message
    message = struct.pack("!icicic", messageId, "x", points1,
                          "o", points2, winner)
    
    # Return the message
    return message

def CreateBoardMessage(gameboard):
    """
    Creates the board message to be sent to the players
    @param gameboard: The complete gameboard of the game
    @type gameboard: List containing characters ('x'/'o'/'-') 100 times
    @return: Returns the message in packed format
             that can then be sent to the client
    @rtype: String
    """
    
    # Define the message ID
    messageId = 22
    
    # Create the message
    message = struct.pack("!i", messageId)
    
    # Pack the values from the game board
    for n in range(0,99):
        struct.pack_into("!c", message, 4+n, gameboard[n])
        
    # Return the message
    return message
    