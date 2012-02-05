'''
Created on Feb 5, 2012

@author: japskua
'''

class Player(object):
    '''
    The Player Object of the player in question
    '''


    def __init__(self, ip, port):
        '''
        Constructor
        '''
        self.ip = ip
        self.port = port
        
        self._marker = None
        self._turn = False
        
    def SetMarker(self, marker):
        self._marker = marker
        
    def GetMarker(self):
        return self._marker
        
    def GetIp(self):
        return self.ip
    
    def GetPort(self):
        return self.port
    
    def SetTurn(self, turn):
        self._turn = turn
        
    def GetTurn(self):
        return self._turn