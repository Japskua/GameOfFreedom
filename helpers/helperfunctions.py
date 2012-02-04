'''
Created on Feb 4, 2012

@author: japskua
'''

import struct

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

def UnpackInteger(messageBuffer, position):
    """
    Unpacks the integer from the message
    from the given position
    @type messageBuffer: String
    @param messageBuffer: The message data that has been received
                          over the web
    @type position: Integer
    @param position: The position where the data in question starts
    @return: The integer taken and the position where the next value can start
    @rtype: Tuple (Integer, Integer)
    """
    # Set the end position to be 4 more than the start one 
    endPosition = position + 4
    
    # Unpack the value and convert to integer
    integer = int(struct.unpack("!i", messageBuffer[position:endPosition])[0])
    
    # Finally, return the integer and the position for next read bit
    return integer, (endPosition+1)

def UnpackChar(messageBuffer, position):
    """
    Unpacks a character from the message buffer
    @type messageBuffer: String
    @param messageBuffer: The message data that has been received
                          over the web
    @type position: Integer
    @param position: The position where the data in question starts
    @return: The character taken and the position where the next value can start
    @rtype: Tuple (Character, Integer)
    """
    # Set the end position to be 1 more than the starting one
    endPosition = position + 1
    
    # Unpack the character
    character = struct.unpack("!c", messageBuffer[position:endPosition])[0]
    
    # Finally, return the character and the position for next read bit
    return character, (endPosition+1)

def UnpackString(messageBuffer, position):
    """
    Unpacks string from the message buffer
    @type messageBuffer: String
    @param messageBuffer: The message data that has been received
                          over the web
    @type position: Integer
    @param position: The position where the data in question starts
    @return: The string taken and the position where the next value can start
    @rtype: Tuple (String, Integer)
    """
    
    # Get the size of the message buffer
    bufferSize = len(messageBuffer)
    
    # Calculate the end position
    endPosition = bufferSize - position
    
    # Unpack the string
    messageString = struct.unpack("!s", messageBuffer[position:endPosition])[0]
    
    # Finally, return the string and the position for next read bit
    return messageString, (endPosition+1)
