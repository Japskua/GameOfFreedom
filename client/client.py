'''
Created on Feb 4, 2012

@author: japskua
'''

import socket
from messager import Messager

# DEFINES
MAX_BUFFER_SIZE = 128

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
        
        # Create the socket
        self.sock = socket.socket(socket.AF_INET, #IPv4
                             socket.SOCK_DGRAM) #UDP
        
        # Create the messager
        self.messager = Messager()
        
    def SendMessage(self, message):
        """
        Sends the message to the server
        
        @param message: The message to be sent
        @type message: String
        """
        if self.verbose:
            print "Sending the message >", message, "< to the server"
        
        # Send the message
        self.sock.sendto(message, (self.host, self.port) )
        
    def JoinServer(self):
        """
        Connects to the server
        """
        # Create the message
        message = self.messager.CreateJoinMessage()
        
        # Send the connecting message to the server
        self.SendMessage(message)
        
        

        