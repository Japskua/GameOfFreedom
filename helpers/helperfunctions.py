'''
Created on Feb 4, 2012

@author: japskua
'''


def AddCarriageLineReturnFeed(message):
    """
    Adds the Carriage Line Return Feed (\r\n) to the
    end of the message in question
    @param message: The message to add the endings
    @type message: String
    @return: The message ready to be sent over the network
    @rtype: String
    """

    # Add the correct endings to the message
    message += "\r\n"
    
    return message