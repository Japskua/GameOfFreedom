'''
Created on Feb 4, 2012

@author: japskua
'''

import socket

class Client(object):
    '''
    classdocs
    '''


    def __init__(self, host, port, verbose):
        '''
        Constructor
        '''
        self.port = port
        self.host = host
        self.verbose = verbose
        
    def SendMessage(self, message):
        """
        Sends the message to the server
        
        @param message: The message to be sent
        @type message: String
        """
        # Create the socket
        sock = socket.socket(socket.AF_INET, #IPv4
                             socket.SOCK_DGRAM) #UDP
        
        # Send the message
        sock.sendto(message, (self.host, self.port) )
        
        
        
        