'''
Created on Feb 4, 2012

@author: japskua
'''

import socket
import select
import sys

from helpers import UnpackInteger, GameBoard
from player import Player
from messages import *
import exceptions
from random import Random

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

    # The server states
    STATE_WAITING = 0
    STATE_PLAYING = 1
    STATE_SCORING = 2

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
        try:
            self.sock = socket.socket(socket.AF_INET,    #IPv4
                                      socket.SOCK_DGRAM) #UDP
        except exceptions:
            print "Unable to create the socket!"
            sys.exit()
            
        # Bind the socket
        try:
            self.sock.bind( (ip, self.port) )
        except exceptions:
            print "Unable to bind the socket"
            sys.exit()
        
        # Create the client listing
        self.listClients = []
        
        # Set own state to waiting
        self.state = Server.STATE_WAITING
        
        # The game related info
        self.activePlayer = 0
        
        # Initialize the game board
        self.gameBoard = GameBoard(self.verbose)
        
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
        
        # MSG_JOIN
        if messageId == 1:
            # If the state is WAITING
            if self.state == Server.STATE_WAITING:
                # Handle the join attempt
                self.HandleClientJoin(addr)
            # Otherwise, send GAME_FULL Error
            else:
                # Create and send the message
                message = CreateErrorMessage(ErrorEnum.ERR_FULL)
                SendMessage(self.sock, addr[0], addr[1], message)
                # And then return
                return
        
        # MSG_PLACE
        elif messageId == 11:
            # If the state in question is playing (otherwise don't react)
            if self.state == Server.STATE_PLAYING:
                # Do something
                pass
            # Otherwise, ignore
            else:
                # Just pass
                pass
        
        # MSG_QUIT
        elif messageId == 40:
            # Quit the player
            
            pass
        
        # Otherwise
        else:
            # Just ignore
            pass
            
    
        # <---------- End of HandleClientInput() -----------> #
        
    def RemovePlayer(self, player):
        """
        Removes the player from the server and nulls the information
        """
        raise NotImplementedError()
        
    def DecidePlayerMarkers(self):
        """
        Randomly chooses the player markers
        """
        
        if self.verbose:
            print "Deciding the player markers"
            
        # Randomly pick number 1 or 0
        random = Random()
        choice = random.randint(0, 1)
        
        # If the choise was 0, set the first player to be X
        if choice == 0:
            self.listClients[0].SetMarker('X')
            self.listClients[1].SetMarker('O')
            # Set the active player to be the first one
            self.activePlayer = 0
        # Otherwise, do the opposite
        else:
            self.listClients[0].SetMarker('O')
            self.listClients[1].SetMarker('X')
            self.activePlayer = 1
            
        # Inform of the choices
        if self.verbose:
            print "Player 1 is", self.listClients[0].GetMarker()
            print "Player 2 is", self.listClients[1].GetMarker()
        
    def HandleClientJoin(self, clientAddress):
        """
        Handles the situation when client tries to join the server
        """
        if self.verbose:
            print "Client", clientAddress, "trying to join the server"
            
        # If there are more than two players already on the server
        if len(self.listClients) >= 2:
            # Create the error message
            message = CreateErrorMessage(ErrorEnum.ERR_FULL)
            # Send a error message
            SendMessage(self.sock, clientAddress[0], clientAddress[1], message)
            # And return
            return
            
        # Otherwise, keep on going
        # Check that neither of the players have the same port (prevent duplicates)
        for playerEntry in self.listClients:
            # If the IP is the same
            if playerEntry.ip == clientAddress[0]:
                # If the port is the same as weell
                if playerEntry.port == clientAddress[1]:
                    # Send error, that the player is already on the server
                    message = CreateErrorMessage(ErrorEnum.ERR_ALREADYJOINED)
                    SendMessage(self.sock, clientAddress[0], clientAddress[1], message)
                    # And return 
                    return
                
        # If that check was passed, create a new player and add him to the list
        player = Player(clientAddress[0], clientAddress[1])
        self.listClients.append(player)
        
        if self.verbose:
            print "Added player:", player.ip, player.port
            print "Server has now", len(self.listClients), "players"
        
        # Create the accept message
        message = CreateAcceptMessage()
        # And send the join message to the player
        SendMessage(self.sock, player.ip, player.port, message)
        
        if self.CheckIfEnoughPlayersJoined() == True:
            # Change the state
            self.ChangeState(self.STATE_PLAYING)
        
        
        # <---------- End of HandleClientJoin() -----------> #
            
    def ChangeState(self, state):
        """
        Handles the changing from one state to another
        Does the required state change operations as well
        """
        
        if self.verbose:
            print "Trying to change the state"
            
        # Check that the state is different than the one currently
        if self.state == state:
            if self.verbose:
                print "The state you are trying to change is the same as current one!"
            # Just return and prevent further changes
            return
        
        # Otherwise, keep on going
        if state == self.STATE_WAITING:
            if self.verbose:
                print "Changing to state", state
            # Do something
            return
        
        elif state == self.STATE_PLAYING:
            if self.verbose:
                print "Changing to state", state
                
            # When changing to playing state, pick the players' markers
            self.DecidePlayerMarkers()
            # Then, Create the game start messages to both of the players
            message1 = CreateGameStartMessage(self.listClients[0].GetMarker())
            message2 = CreateGameStartMessage(self.listClients[1].GetMarker())
            # And send the messages
            SendMessage(self.sock, self.listClients[0].GetIp(), self.listClients[0].GetPort(), message1)
            SendMessage(self.sock, self.listClients[1].GetIp(), self.listClients[1].GetPort(), message2)
            
            # Create the board
            self.gameBoard.CreateBoard()
            # And display it
            self.gameBoard.DisplayBoard()
            # Finally, send the game started message to the first player
            return
        
        elif state == self.STATE_SCORING:
            if self.verbose:
                print "Changing to state", state
            # Do something
            return
        
        else:
            if self.verbose:
                print "Received something weird as state change!", state
            # Just return
            return
        
        
                
    def CheckIfEnoughPlayersJoined(self):
        """
        Checks if enough players (2) have joined to the server
        @return: True if all players joined, False otherwise
        @rtype: Boolean
        """
        if len(self.listClients) == 2:
            return True
        else:
            return False
        
        