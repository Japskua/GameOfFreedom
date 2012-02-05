'''
Created on Feb 4, 2012

@author: japskua
'''

import socket
import select
import sys

from helpers import UnpackInteger, UnpackChar, GameBoard
from player import Player
from messages import *
import exceptions
from random import Random
from warnings import catch_warnings

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
    
    MAX_TURNS = 2

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
        
        self.turn = 1
        
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
            print "self.state is", self.state
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
            if self.verbose:
                print "Received message 11 - State is:", self.state
            # If the state in question is playing (otherwise don't react)
            if self.state == Server.STATE_PLAYING:
                # Check that the message came from correct player
                if self.CheckCorrectPlayer(addr) == True:
                    # If everything was okay
                    # Handle the player Movement
                    self.HandlePlayerPlacement(data, position)
                
               
            # Otherwise, ignore
            else:
                # Just pass
                pass
        
        # MSG_QUIT
        elif messageId == 40:
            # Quit the player
            
            # Check if the player was found
            if (self.FindPlayer(addr) != False):
            
                # Figure who was the player that sent the message
                player = self.FindPlayer(addr)
                self.RemovePlayer(player)
                
                # Send the victory message to the other player
                self.InformPlayerForfeit()
        
        # Otherwise
        else:
            # Just ignore
            pass
            
    
        # <---------- End of HandleClientInput() -----------> #
        
    def InformPlayerForfeit(self):
        """
        Informs the other player that player has left the game
        and forfeited.
        """
        
        message = CreateGameEndMessage(GameEndReasonEnum.PLAYER_LEFT)
        
        # Send the message to the client left
        SendMessage(self.sock, self.listClients[0].GetIp(), self.listClients[0].GetPort(), message)
        
        # Remove the other player as well
        self.RemovePlayer(0)
        
        self.Clean()
        
    def Clean(self):
        """
        Cleans everything once the players are gone
        """
        self.turn = 1
        self.activePlayer = 0
        self.gameBoard.CreateBoard()
        self.listClients = []
        self.state = Server.STATE_WAITING
        
        
        
    def FindPlayer(self, addr):
        """
        Finds the number of the player in question
        @return: Number of the client in question if found
                 False if nothing was found
        """
        # Loop through all the clients
        for clientNumber in range(0,2):
            # Check if the IP matches
            try:
                if self.listClients[clientNumber].GetIp() == addr[0]:
                    # Check if the port matches
                    if self.listClients[clientNumber].GetPort() == addr[1]:
                        # Return the client number
                        return clientNumber
            except Exception:
                pass
            
                
        return False
                    
    
    def HandlePlayerPlacement(self, data, position):
        """
        Handles the player movement
        """
        if self.verbose:
            print "Handling the player placement"
        
        # Get the player placement from the message
        marker, position = UnpackChar(data, position)
        
        # Get the placement from the message
        placement, position = UnpackInteger(data, position)
        
        # Try to place the marker
        if self.gameBoard.TryPlaceMarker(placement, marker) == False:
            # Send wrong placement message
            message = CreateErrorMessage(ErrorEnum.ERR_PLACEMENT)
            SendMessage(self.sock, self.listClients[self.activePlayer].GetIp(), 
                        self.listClients[self.activePlayer].GetPort(), message)
            
        else:
            # Change the turn to the other player
            self.NextTurn()
        
    def NextTurn(self):
        """
        Changes the turn to the next player
        """
        # Advance the turns by one
        self.IncrementTurns()
        
        # Check if this was the last turn
        if self.turn == Server.MAX_TURNS:
            # Send message for game end
            message = CreateErrorMessage(GameEndReasonEnum.TURNS_FULL)
            # Send the message
            SendMessage(self.sock, self.listClients[0].GetIp(), self.listClients[0].GetPort(), message)
            SendMessage(self.sock, self.listClients[1].GetIp(), self.listClients[1].GetPort(), message)
            
            # Then, change state to SCORING
            self.ChangeState(Server.STATE_SCORING)
            return
            
        # Otherwise, keep on going
        
        # Send the board message to both of the players
        self.SendBoardMessage()
        
        # Change the player
        self.ChangePlayer()
        
        # Send the turn to the next player
        self.SendTurnMessage()
        
        
    def ChangePlayer(self):
        """
        Changes the active player to the second one
        """
        
        # If the current active player was number 1
        if self.activePlayer == 0:
            # Set the turn for the current player false
            self.listClients[0].SetTurn(False)
            # And true for the other player
            self.listClients[1].SetTurn(True)
            self.activePlayer = 1
        elif self.activePlayer == 1:
            # Set the turn for the current player false
            self.listClients[1].SetTurn(False)
            # And true for the other player
            self.listClients[0].SetTurn(True)
            self.activePlayer = 0

                
        if self.verbose:
            print "Changed active player to player number", self.activePlayer
        
    def IncrementTurns(self):
        """
        Adds 1 to the turns
        """
        self.turn += 1
    
    def CheckCorrectPlayer(self, addr):
        """
        Checks that the message received is from the correct player
        """    
        userIp = addr[0]
        userPort = addr[1]
        
        # Check if the ip is the correct one
        if userIp != self.listClients[self.activePlayer].GetIp():
            return False
        
        if userPort != self.listClients[self.activePlayer].GetPort():
            return False
        
        # Otherwise, the right client send the message
        return True
    
    def RemovePlayer(self, playerNumber):
        """
        Removes the player from the server and nulls the information
        """
        # Search for the player that has the same port
        print playerNumber
        player = self.listClients[playerNumber]

        # Create the quit message
        message = CreateQuitMessage()
        # Send the message
        SendMessage(self.sock, player.GetIp(), player.GetPort(), message)
        
        # And finally remove the player from the list
        self.listClients.remove(player)

        
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
            
            # Remove the players from the list
            for player in self.listClients:
                self.listClients.remove(player)
            
            # Cleanup everything
            self.Clean()
                
            # Change the state
            self.state = Server.STATE_WAITING
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
            
            # Send the board message to both of the players
            self.SendBoardMessage()
            
            # Then, send the turn to player number 1
            self.SendTurnMessage()
            
            # And finally, change the state
            self.state = state
                        
            if self.verbose:
                print "State is now:", self.STATE_PLAYING
            return
        
        elif state == self.STATE_SCORING:
            if self.verbose:
                print "Changing to state", state
                
            # Calculate the scores
            player1Score, player2Score = self.gameBoard.CalculateScore()
            
            winner = "-"
            
            # Get the winner
            if player1Score > player2Score:
                winner = "X"
            elif player2Score > player1Score:
                winner = "O"
            else:
                winner = "-"
            
            # Create the score message
            scoreMessage = CreateScoreMessage(player1Score, player2Score, winner)
            # Send the message to both of the players
            SendMessage(self.sock, self.listClients[0].GetIp(), self.listClients[0].GetPort(), scoreMessage)
            SendMessage(self.sock, self.listClients[1].GetIp(), self.listClients[1].GetPort(), scoreMessage)
            
            # And change back to waiting state
            self.ChangeState(Server.STATE_WAITING)
            return
        
        else:
            if self.verbose:
                print "Received something weird as state change!", state
            # Just return
            return
        
    
        
    def SendTurnMessage(self):
        """
        Sends the turn message to the correct player
        """
        if self.verbose:
            print "Creating the turn message"
            
        # Get the free places
        listPlaces = self.gameBoard.GetNextPossiblePlacement()
        
        # Create a message with the proper amount of placements
        message = CreateTurnMessage(listPlaces, True)
        
        # Send the message to the client
        SendMessage(self.sock, self.listClients[self.activePlayer].GetIp(), 
                    self.listClients[self.activePlayer].GetPort(), message)

        # Done sending the message
        
    def SendBoardMessage(self):
        """
        Sends the board message to both of the players
        """
        if self.verbose:
            print "Creating the board message"
            
        self.gameBoard.DisplayBoard()
        # Create the message
        boardMessage = CreateBoardMessage(self.gameBoard.GetBoard())
        
        # Send the message to both of the players
        SendMessage(self.sock, self.listClients[0].GetIp(), self.listClients[0].GetPort(), boardMessage)
        SendMessage(self.sock, self.listClients[1].GetIp(), self.listClients[1].GetPort(), boardMessage)
                
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
        
        