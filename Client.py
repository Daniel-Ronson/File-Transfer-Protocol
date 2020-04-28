from socket import *
from random import randint
from random import seed

import sys
#user supplied values, command line arguments
try:
    serverName = sys.argv[1]
    serverPort = sys.argv[2]

#default values
except:
    serverName = "localhost"
    serverPort = 21

controlSocket = socket(AF_INET,SOCK_STREAM)

#Connect to Server, assumed Server is listening
controlSocket.connect((serverName,serverPort))

#client sends a unique value to authenticate
#this value is also a session id
#convert random int to string
seed(1)
userToken = str(randint(1,1000))

dataPort = 0;
def establish_control_connection():
    bytesSent = 0
    while bytesSent != len(userToken):

        bytesSent += controlSocket.send(userToken.encode()[bytesSent:])

        #recieve response from server
        dataSize = bytes()
        dataPort = controlSocket.recv(1024).decode()

    print("Establishing Control Connection: ", dataPort)


def list_files():
    # send 'ls' to the server
    controlSocket.send(userInput.encode())

    # server responds with the new data port
    dataPort = int(controlSocket.recv(1024).decode())

    # Connect to Data Socket on server
    dataSocket = socket(AF_INET, SOCK_STREAM)
    dataSocket.connect((serverName, dataPort))

    # wait for server to send requested list of files
    msg = dataSocket.recv(1024).decode()
    print(msg)
    dataSocket.close()
#-----main-------------------

#establish connection
establish_control_connection();

keep_open = True
while keep_open:
    userInput = input("ftp>")
    if userInput == 'quit':
        keep_open = False
    elif userInput== 'get':
        break;
    elif userInput == 'ls':
        list_files()

controlSocket.close()
