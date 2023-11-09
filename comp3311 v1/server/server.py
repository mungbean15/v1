import json
import sys
from socket import *
from typing import Dict

from ClientThread import ClientThread
from s_helper import (s_check_arguments,
                      s_check_serverPort,
                      s_check_failAttempts,
                      read_credentials
                      )


## CHECKS FOR IF THE EXECUTION IS EXECUTABLE ##
s_check_arguments(sys.argv)

LOCALHOST = "127.0.0.1"
serverPort = int(sys.argv[1])
FAILATTEMPTS = int(sys.argv[2])

s_check_serverPort(serverPort)
s_check_failAttempts(FAILATTEMPTS)


## SPECIAL VARIABLES ##
clientMap: Dict[str, str] = dict()
clientMap = read_credentials(clientMap)


## MAKE SURE NETWORK IS EMPTY AT START UP ##
uploadLog = 'upload-log.txt'
edLog = 'edge-device-log.txt'
deletionLog = 'deletion-log.txt'
blockedLog = 'blocked.txt'
with open(uploadLog, 'w') as file:
    pass
with open(edLog, 'w') as file:
    pass
with open(deletionLog, 'w') as file:
    pass
with open(blockedLog, 'w') as file:
    pass


## START UP SERVER ##
# define socket for the server side and bind address
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((LOCALHOST, serverPort))


print("\n===== Server is running =====")
print("===== Waiting for connection request from clients...=====")


while True:
    serverSocket.listen()
    clientSockt, clientAddress = serverSocket.accept()
    clientThread = ClientThread(clientAddress, clientSockt, clientMap, FAILATTEMPTS)
    clientThread.start()
