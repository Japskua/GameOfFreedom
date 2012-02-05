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
from helpers import UnpackInteger, UnpackChar, GameBoard

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
    
    STATE_IDLE = 0
    STATE_WAITING = 1
    STATE_PLAYING = 2
    STATE_SCORING = 3

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
        self.gameboard = GameBoard(self.verbose)
        self.gameboard.CreateBoard()
        self.gameboard.DisplayBoard()
        
        # Set own state to be idle
        self.state = Client.STATE_IDLE
        
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
        messageBuffer, addr = self.sock.recvfrom(MAX_BUFFER_SIZE)
        
        if messageBuffer == None:
            return 
        
        if self.verbose:
            print "Received:", messageBuffer, "from", addr
            
        # Create the buffer pointer
        pointer = 0
        # Try to unpack the received info
        messageId, pointer = UnpackInteger(messageBuffer, pointer)
        
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
            # Set own state to be waiting
            self.state = Client.STATE_WAITING
            print "Connection created Succesfully. Now waiting for the game to start..."
            
        
        # MSG_GAME_START
        elif messageId == 3:
            print "Game Started!"
            # Get the player marker
            self.marker, pointer = UnpackChar(messageBuffer, pointer)
            # Inform the player of the assigned marker
            print "You are now playing with marker:", self.marker
            # Set own state to be playing
            self.state = Client.STATE_WAITING
        
        # MSG_TURN
        elif messageId == 10:
            # Get the size of the received message
            freePlaces, pointer = UnpackInteger(messageBuffer, pointer)
        
            print "You have", freePlaces, "free places to put your marker"
          
            # Empty the previous availablePosition list
            self.availablePosition = []
            
            # Loop through all the free places
            for i in range(0,freePlaces):
                # Get the value in question
                value, pointer = UnpackInteger(messageBuffer, pointer)
                self.availablePosition.append(value)
                
            # And then display all the available position
            for entry in self.availablePosition:
                print entry
        
        # MSG_SCORE
        elif messageId == 20:
            marker1, pointer = UnpackChar(messageBuffer, pointer)
            points1, pointer = UnpackInteger(messageBuffer, pointer)
            marker2, pointer = UnpackChar(messageBuffer, pointer)
            points2, pointer = UnpackInteger(messageBuffer, pointer)
            winner, pointer = UnpackChar(messageBuffer, pointer)
            
            print "Player", marker1, "scored", points1, "points."
            print "Player", marker2, "scored", points2, "points."
            print "The winner of the game was:", winner
            
            # And then set own state back to idle
            self.state = Client.STATE_IDLE
            
        
        # MSG_GAME_END
        elif messageId == 21:
            # Get the reason for the end of the game
            endReason, pointer = UnpackInteger(messageBuffer, pointer)
            
            # Inform the player of the end reaons
            if endReason == Client.ENDTYPE_LEAVE:
                print "Player Left"
                
            elif endReason == Client.ENDTYPE_TURNS:
                print "Turns full"
                
            # Set own state to be scoring
            self.state = Client.STATE_SCORING
                
        
        # MSG_BOARD
        elif messageId == 22:
            # Get the situation of the board
            for i in range(0, 99):
                # Get the value on the board
                symbol, pointer = UnpackChar(messageBuffer, pointer)
                self.board.append(symbol)
                
            # Then, display the board
            self.DisplayBoard()
        
        # MSG_ERROR
        elif messageId == 30:
            # Get the error type
            errorType, pointer = UnpackInteger(messageBuffer, pointer)
            
            # Check what it was
            if errorType == 1:
                print "Wrong Placement!"
            elif errorType == 2:
                print "Server Full!"
            elif errorType == 3:
                print "Already on the server!"
            
            # An unknown error code was received
            else:
                print "Undefined error code:", errorType
        
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
        
        

        