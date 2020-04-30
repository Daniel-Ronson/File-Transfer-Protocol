from socket import *
from random import randint
from random import seed

import sys

# user supplied values, command line arguments
try:
    serverName = sys.argv[1]
    serverPort = sys.argv[2]

# default values
except:
    serverName = "localhost"
    serverPort = 21

controlSocket = socket(AF_INET, SOCK_STREAM)

# Connect to Server, assumed Server is listening
controlSocket.connect((serverName, serverPort))

# client sends a unique value to authenticate
# this value is also a session id
# convert random int to string
seed(1)
userToken = str(randint(1, 1000))

dataPort = 0


def testCase():
    print("works")


def establish_control_connection():
    global dataPort
    bytesSent = 0
    while bytesSent != len(userToken):
        bytesSent += controlSocket.send(userToken.encode()[bytesSent:])

        # recieve response from server
        dataSize = bytes()
        dataPort = controlSocket.recv(1024).decode()

    print("Establishing Control Connection: ", dataPort)


def getFileInfo(filename):
    fileObj = open(filename, "r")
    fileData = fileObj.read(65536)
    filesize = 0
    testCase()
    if fileData:
        filesize = str(len(fileData))
        while len(filesize) < 10:
            filesize = "0" + filesize
            print(filesize + " the file size")
            testCase()

    fileData = filesize + fileData
    testCase()
    return fileData


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


# -----main-------------------

# establish connection
establish_control_connection();

keep_open = True
while keep_open:
    userInput = input("ftp> ")
    user = userInput.split(" ")
    if user[0] == 'quit':
        keep_open = False
    elif user[0] == 'get':
        break
    elif user[0] == 'put':
        filename = user[1]
        # print(filename)
        fileinfo = getFileInfo(filename)
        controlSocket.send(userInput.encode())
        newPort = int(controlSocket.recv(1024).decode())
        newSock = socket(AF_INET, SOCK_STREAM)
        newSock.connect((serverName, newPort))
        # print(fileinfo + "The file info")
        numBytes = 0
        while len(fileinfo) > numBytes:
            numBytes += newSock.send(fileinfo[numBytes].encode())

    elif user[0] == 'ls':
        list_files()

controlSocket.close()
