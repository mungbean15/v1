import json
from threading import Thread
from time import time
from typing import Dict

from s_helper import (create_blockedMap)


"""
    Multi-thread class for client
    Code from example provided on webcms
"""
class ClientThread(Thread):
    def __init__(self, clientAddress, clientSocket, clientMap, failAttempts):
        Thread.__init__(self)
        self.clientAddress = clientAddress
        self.clientSocket = clientSocket
        self.clientMap = clientMap
        self.failAttempts = failAttempts

        self.clientAlive = False
        self.clientBlock = False
        self.consecutiveFails = 0
        self.username = ''
        self.s_message = dict()

        self.clientAlive = True
        print("New connection created for:", clientAddress)
    
        
    def run(self):
        while self.clientAlive:
            blockedMap: Dict[str, int] = dict()
            blockedMap = create_blockedMap(blockedMap)

            data = self.clientSocket.recv(1024)
            self.update(blockedMap)

            if not data:
                self.clientAlive = False
                print("Edge device with address '" + str(self.clientAddress) + "' has exited the edge network")
                exit(0)

            data = json.loads(data.decode())
            self.username = data['username']
            recv_command = data['command']

            # server message to client
            self.s_message['command'] = str(data['command'])

            if recv_command == 'LOGIN':
                self.s_message['attempts_left'] = self.failAttempts
                print("[recv] New login request.")
                self.login_command(data)
                print(self.s_message)
                self.clientSocket.sendall(json.dumps(self.s_message).encode())
            # elif ENTER OTHER COMMANDS


    def update(self, blockedMap):
        if self.username in blockedMap and 10 + blockedMap[self.username] < time():
            with open('blocked.txt', 'r') as f:
                lines = f.readlines()
            with open('blocked.txt', 'w') as f:
                for line in lines:
                    if line.strip() != self.username:
                        f.write(line)


    def login_command(self, data, blockedMap):
        password = data['password']
        status = self.auth(password, blockedMap)
        self.s_message['status'] = str(status)
    

    def auth(self, password, blockedMap):
        if self.username not in self.clientMap:
            return 'INVALID_USERNAME'
        
        if self.username in blockedMap:
            return 'BLOCKED'
        
        if password != self.clientMap[self.username]:
            self.consecutiveFails += 1
            self.s_message['attempts_left'] -= 1

            if self.consecutiveFails >= self.failAttempts:
                print("in being blocked")
                print("[send] Edge device", self.username, "has been blocked from the network.")

                # add username and their blocked time to blocked.txt file
                f = open('blocked.txt', 'a')
                message = self.username + ' ' + str(time())
                f.write(message + '\n')
                f.close

                return 'BLOCKING'
            return 'INVALID_PASSWORD'
            
        self.consecutiveFails = 0
        self.blockedSince = 0
        print("[send] Edge device", self.username, "has joined the network.")
        # TODO: add to file
        # NOTE: how to keep track of all active users?
        return 'SUCCESS'
    


        
