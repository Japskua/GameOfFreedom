'''
Created on Feb 5, 2012

@author: japskua
'''

import struct

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