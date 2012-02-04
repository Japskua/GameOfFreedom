'''
Created on Feb 4, 2012

@author: Japskua
'''

from server import Server
import getopt
import sys

version = '1.0'
verbose = True
port = 100
host = "100.0"

output_filename = 'output.log'

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
    print "Starting the server..."

# Create the server class and put it to run
freedom_server = Server(port, verbose)
freedom_server.ShowArgs()
freedom_server.StartServer()