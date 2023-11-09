"""
    Python 3
    Usage: python3 TCPClient3.py localhost 12000
    coding: utf-8
    
    Author: Wei Song (Tutor for COMP3331/9331)
"""
import json
import sys
from socket import *

from c_helper import (c_check_arguments,
                      c_check_server_port,
                      c_check_UDP_port)


## CHECK ARGUMENTS WHEN EXECUTING ##
c_check_arguments(sys.argv)

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
UDPPort = int(sys.argv[3])

c_check_server_port(serverPort)
c_check_UDP_port(UDPPort)


## CONNECT CLIENT TO SERVER ##
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))

username = ''
password = ''
c_message = json.dumps({
                'command': 'LOGIN',
                'username': username,
                'password': password,
                'serverPort': serverPort,
                'UDPPort': UDPPort
            })
c_message = json.loads(c_message)

## AUTHENTICATION ##
def log_in():
    global c_message

    while c_message['username'] == '':
        c_message['username'] = input('Username: ')
    while c_message['password'] == '':
        c_message['password'] = input('Password: ')

    return send_and_receive(c_message) 

def send_and_receive(message):
    global c_message

    # print('[send]',message)
    clientSocket.sendall(json.dumps(message).encode())
    reply = clientSocket.recv(1024)
    # print('[recv]', json.loads(reply))

    return json.loads(reply.decode())


def authentication():
    global c_message

    reply = log_in()
    while reply['command'] == 'LOGIN':
        if reply['status'] == 'SUCCESS':
            print('You are logged in. Welcome', c_message['username'] + '!\n')
            interact()
        elif reply['status'] == 'INVALID_PASSWORD':
            print('Invalid password. You have', reply['attempts_left'], 'attempt(s) left. Please try again.\n')
            c_message['password'] = input('Password: ')
            reply = send_and_receive(c_message)
        elif reply['status'] == 'BLOCKING':
            print('Invalid password. Your account has been blocked. Please try again later.\n')
            exit(0)
        elif reply['status'] == 'BLOCKED':
            print('Your account has been blocked due to multiple authentication failures. Please try again later.\n')
            exit(0)
        elif reply['status'] == 'INVALID_USERNAME':
            print('This user does not exist. Please try again.\n')
            c_message['username'] = ''
            c_message['password'] = ''
            reply = log_in()
        else:
            print('FATAL: unexpected message\n')
            exit(1)


def interact():
    global c_message

    while True:
        commandPromt = "Please enter one of the following commands:\n\tAED - list active edge devices\n\tDTE - delete data file from server\n\tEDG - generate edge data\n\tOUT - exit network\n\tSCS - use server computation service\n\tUED - upload edge data to server\n\tUVF - send video file to edge device\n"
        message = input(commandPromt)
        clientSocket.sendall(message.encode())

        # receive response from the server
        # 1024 is a suggested packet size, you can specify it as 2048 or others
        data = clientSocket.recv(1024)
        receivedMessage = data.decode()

        # parse the message received from server and take corresponding actions
        if receivedMessage == "":
            print("[recv] Message from server is empty!")
        elif receivedMessage == "user credentials request":
            print("[recv] You need to provide username and password to login")
        elif receivedMessage == "download filename":
            print("[recv] You need to provide the file name you want to download")
        elif receivedMessage == "logout":
            print("[recv] You are now logged out.")
            break
        else:
            print("[recv] Message makes no sense")
            
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break
    # close the socket
    clientSocket.close()

if __name__ == '__main__':
    authentication()
