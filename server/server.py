'''
Created on Feb 4, 2012

@author: japskua
'''

import socket

ip = "127.0.0.1"

# Buffer size
MAX_BUFFER_SIZE = 128

class Server(object):
    '''
    classdocs
    '''


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
        
        # Create the socket for the datagram
        sock = socket.socket(socket.AF_INET,    #IPv4
                             socket.SOCK_DGRAM) #UDP
        
        # Bind the socket
        sock.bind( (ip, self.port) )
        
        if self.verbose:
            print "Server ready to listen"
        
        # Start running
        while True:
            data, addr = sock.recvfrom(MAX_BUFFER_SIZE)
            print "Received message:", data[:-2]
            print "From:", addr
            
            print "Message length was", len(data)
            
    
        
        