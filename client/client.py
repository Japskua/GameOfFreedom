'''
Created on Feb 4, 2012

@author: japskua
'''

"""
Sources:
http://docs.python.org/howto/sockets.html
http://code.activestate.com/recipes/531824-chat-server-client-using-selectselect/
http://docs.python.org/library/struct.html
http://www.rhinocerus.net/forum/lang-python/577763-unpack-expects-wrong-number-bytes.html

BEST ONE!!!
http://docs.python.org/library/select.html#select.select
"""

import socket
from messager import Messager
import select
from keyboardcontroller import KeyboardController
import struct
from helpers import UnpackInteger

# DEFINES
STDIN = 0
MAX_BUFFER_SIZE = 128

RUNNING = True

class Client(object):
    '''
    classdocs
    '''
    ENDTYPE_TURNS = 0
    ENDTYPE_LEAVE = 1

    def __init__(self, host, port, verbose):
        '''
        Constructor
        '''
        self.port = port
        self.host = host
        self.verbose = verbose
        self.marker = "x"
        
        # Create the socket
        self.sock = socket.socket(socket.AF_INET, #IPv4
                             socket.SOCK_DGRAM) #UDP
        
        # Create the messager
        self.messager = Messager(self.verbose)
        # Create the keyboard controller
        self.keyboardController = KeyboardController(self.verbose)
        
        # Create a list to hold the available positions
        self.availablePosition = []
        
        # Create the board
        self.board = []
        
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
                    message = self.keyboardController.ReadInput(self.marker)
                    # If other than None was received
                    if message != None:
                        # send the generated message to the server
                        self.SendMessage(message)
                    
                    
                # If there is data coming from the socket
                elif interface == self.sock:
                    self.HandleServerInput()
        
        
    def HandleServerInput(self):
        """
        Handles all the messages received from the server
        """
        # Receive the data
        data, addr = self.sock.recvfrom(MAX_BUFFER_SIZE)
        
        if data == None:
            return 
        
        if self.verbose:
            print "Received:", data, "from", addr
            
        # Try to unpack the received info
        messageId = int(struct.unpack("!i", data[0:4])[0])
        
        if self.verbose:
            print "MessageID:", messageId
            
        # Then, act accordingly
        #################################
        # VALUES THAT CAN BE RECEIVED FROM THE SERVER
        # 2 - MSG_ACCEPT
        # 3 - MSG_GAME_START
        # 10 - MSG_TURN
        # 20 - MSG_SCORE
        # 21 - MSG_GAME_END
        # 22 - MSG_BOARD
        # 30 - MSG_ERROR
        ################################
        
        # MSG_ACCEPT
        if messageId == 2:
            # Accepted to the game
            print "Connection created Succesfully. Now waiting for the game to start..."
        
        # MSG_GAME_START
        elif messageId == 3:
            print "Game Started!"
            
            # Get the player marker
            self.marker = struct.unpack("!c", data[5:6])[0]
            # Inform the player of the assigned marker
            print "You are now playing with marker:", self.marker
        
        # MSG_TURN
        elif messageId == 10:
            # Get the size of the received message
            freePlaces = int(struct.unpack("!i", data[5:8])[0])
        
            print "You have", freePlaces, "free places to put your marker"
          
            # Empty the previous availablePosition list
            self.availablePosition = []
            
            # Loop through all the free places
            for i in range(0,freePlaces):
                # Get the value in question
                start = 9+i*3
                end = start+3
                value = int(struct.unpack("!i", data[start:end])[0])
                self.availablePosition.append(value)
                
            # And then display all the available position
            for entry in self.availablePosition:
                print entry
        
        # MSG_SCORE
        elif messageId == 20:
            marker1 = struct.unpack("!c", data[5:6])[0]
            points1 = int(struct.unpack("i", data[7:10])[0])
            marker2 = struct.unpack("!c", data[11:12])[0]
            points2 = int(struct.unpack("i", data[13:16])[0])
            winner = struct.unpack("!c", data[17:18])[0]
            
            print "Player", marker1, "scored", points1, "points."
            print "Player", marker2, "scored", points2, "points."
            print "The winner of the game was:", winner
            
        
        # MSG_GAME_END
        elif messageId == 21:
            # Get the reason for the end of the game
            endReason = int(struct.unpack("!i", data[5:8])[0])
            
            # Inform the player of the end reaons
            if endReason == Client.ENDTYPE_LEAVE:
                print "Player Left"
                
            elif endReason == Client.ENDTYPE_TURNS:
                print "Turns full"
                
        
        # MSG_BOARD
        elif messageId == 22:
            # Get the situation of the board
            for i in range(0, 99):
                # Get the value on the board
                start = i+5
                end = start + 1
                symbol = int(struct.unpack("!c", data[start:end])[0])
                self.board.append(symbol)
                
            # Then, display the board
            self.DisplayBoard()
        
        # MSG_ERROR
        elif messageId == 30:
            # Get the error type
            errorType = int(struct.unpack("!i", data[5:9])[0])
            # And get the error message
            errorMessage = struct.unpack("!s", data[10:len(data)-1])[0]
            
            # Check what it was
            if errorType == 1:
                print "Wrong Placement!"
                print "Error:", errorMessage
            elif errorType == 2:
                print "Server Full!"
                print "Error", errorMessage
        
        # Something else was received
        else:
            # Just stay quiet
            pass
                
        
    def DisplayBoard(self):
        i = 0
        for entry in self.board:
            print i, entry
    
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
        
        

        