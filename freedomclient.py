'''
Created on Feb 4, 2012

@author: japskua
'''

from client import Client
import getopt
import sys

version = '1.0'
verbose = False
port = 100
host = "100.0"

output_filename = 'output_client.log'

## Get the command line arguments
options, remainder = getopt.getopt(sys.argv[1:], 'h:p:v', ['host=', 
                                                         'verbose',
                                                         'port=',
                                                         ])

# Check if all the values are defined
for opt, arg in options:
    if opt in ('-h', '--host'):
        host = arg
    elif opt in ('-v', '--verbose'):
        verbose = True
    elif opt in ("-p", '--port'):
        port = int(arg)

if verbose:
    print "Starting the Client..."

# Create the server class and put it to run
freedom_client = Client(host, port, verbose)
freedom_client.JoinServer()
#freedom_client.SendMessage("Hei Serveri!")