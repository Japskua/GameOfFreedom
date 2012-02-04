'''
Created on Feb 5, 2012

@author: japskua
'''

class Player(object):
    '''
    classdocs
    '''


    def __init__(self, ip, port):
        '''
        Constructor
        '''
        self.ip = ip
        self.port = port
        
        self.marker = None
        
    def SetMarker(self, marker):
        self.marker = marker
        
    def GetMarker(self):
        return self.marker
        