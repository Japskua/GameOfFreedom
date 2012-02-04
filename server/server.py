'''
Created on Feb 4, 2012

@author: japskua
'''

import socket
import select
import sys

from helpers import UnpackInteger

ip = ""

# DEFINES

# Keyboard input
STDIN = 0
# Buffer size
MAX_BUFFER_SIZE = 128

server_running = True

class Server(object):
    '''
    classdocs
    '''
    
    command_quit = "/quit"


    def __init__(self, port, verbose):
        '''
        Constructor
        @param port: Port to which the server listens to
        @type port: Integer
        @param verbose: If this value is set to True, the server
                        displays additional information
        @type verbose: Boolean
        '''
        self.port = port
        self.verbose = verbose
        
        # Initialize the socket
        self.sock = socket.socket(socket.AF_INET,    #IPv4
                                  socket.SOCK_DGRAM) #UDP
        
        # Bind the socket
        self.sock.bind( (ip, self.port) )
        
        # Create the client listing
        self.listClients = []
        
        if self.verbose:
            print "Server Created Successfully!"
        
    def ShowArgs(self):
        """
        Displays the important values of the server
        """
        print "Port=", self.port
        
    def StartServer(self):
        """
        Creates all the server required stuff (e.g. creating
        and binding the sockets, etc.)
        
        Starts the server main loop
        """
        
        server_running = True
        
        if self.verbose:
            print "Server ready to listen"
            
        while server_running == True:
            # Create the select
            # Read interface is the only one existing (no errors nor writes)
            # The read interfaces are the keyboard input and the UDP socket
            input_interfaces = select.select([STDIN, self.sock], [], [])[0]
            
            # Check if any of the interfaces contain anything
            for interface in input_interfaces:
            
                # If there is any keyboard input coming
                if interface == STDIN:
                    # Get the data from the keyboard
                    server_running = self.HandleKeyboardInput()
                    
                    
                # If there is data coming from the socket
                elif interface == self.sock:
                    self.HandleClientInput()
                    
        # After the server is over
        print "Server Quiting..."
                    
    def HandleKeyboardInput(self):
        """
        Handles the keyboard input received from the
        server "admin" ;-)
        NOTE: Only command existing is /quit
        @return: False if the quit command was given
                 True otherwise
        @rtype: Boolean
        """
        
        # First, read the keyboard input
        keyboardInput = sys.stdin.readline()
        
        if self.verbose:
            print "The command given was", keyboardInput
        
        # Then, check if the /quit command was given
        if keyboardInput.startswith(Server.command_quit):
            return False
        
        # Otherwise, just return false
        return True
    
        
        

    def HandleClientInput(self):
        """
        Handles the input received from the client [from the socket]
        """
        
        # Receive the data
        data, addr = self.sock.recvfrom(MAX_BUFFER_SIZE)
        
        # If nothing was received, just go back
        if data == None:
            return 
        
        if self.verbose:
            print "Received:", data, "from", addr
            
        # Try to unpack the received info
        #messageId = int(struct.unpack("!i", data[0:4])[0])
        position = 0
        messageId, position = UnpackInteger(data, position)
        
        if self.verbose:
            print "MessageID:", messageId
        
        # Then, act accordingly
        #################################
        # VALUES THAT CAN BE RECEIVED FROM THE CLIENT
        # 1 - MSG_JOIN
        # 11 - MSG_PLACE
        # 40 - MSG_QUIT
        ################################
        
        
            
    
        
        