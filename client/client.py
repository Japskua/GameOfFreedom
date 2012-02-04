'''
Created on Feb 4, 2012

@author: japskua
'''

import socket
from messager import Messager
import select
from keyboardcontroller import KeyboardController

# DEFINES
STDIN = 0
MAX_BUFFER_SIZE = 128

RUNNING = True

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
        # Create the keyboard controller
        self.keyboardController = KeyboardController()
        
    def StartClient(self):
        """
        Starts the main loop of the client
        that handles both server and keyboard input
        """
        
        while True:
            # Create the select
            # Read interface is the only one existing (no errors nor writes)
            # The read interfaces are the keyboard input and the server response
            input_interfaces = select.select([STDIN, self.sock], [], [])[0]
            
            # Check if any of the interfaces contain anything
            for interface in input_interfaces:
            
                # If there is any keyboard input coming
                if interface == STDIN:
                    # Get the data from the 
                    self.keyboardController.ReadInput()
                    
                    
                # If there is data coming from the socket
                elif interface == self.sock:
                    # Receive the data
                    data, addr = self.sock.recvfrom(MAX_BUFFER_SIZE)
                    print "Received:", data, "from", addr
        
    def Placement(self):
        
        message = self.messager.CreatePlaceMessage("x", 54)
        self.SendMessage(message)
        
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
        
        

        