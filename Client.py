from socket import *
from random import randint
from random import seed
import os
import sys
import json

# user supplied values, command line arguments
try:
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])

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
    try:
        path = './localStorage/' + filename
        fileSize = os.path.getsize(path)
        fileObj = open(path)
        fileData = fileObj.read(fileSize)
        filesize = 0
        if fileData:
            filesize = str(len(fileData))
            while len(filesize) < 10:
                filesize = "0" + filesize

        fileData = filesize + fileData
        return fileData
    except:
        return -1

def recFile(sock, bytes):
    recBuff = ""
    tmpBuff = ""
    # print(bytes)
    while len(recBuff) < bytes:
        tmpBuff = sock.recv(bytes)
        # print(tmpBuff)
        if not tmpBuff:
            break
        recBuff += tmpBuff.decode()
        # print(recBuff)

    return recBuff

def mkFile(filename, fileData):
    newPath = "./localStorage/" + filename
    f = open(newPath, "w+")
    f.write(fileData)
    os.fsync(f.fileno())
    f.close()

def get_list_files():
    # send 'ls' to the server
    controlSocket.send(userInput.encode())
    # server responds with the new data port
    dataPort = int(controlSocket.recv(1024).decode())
    # Connect to Data Socket on server
    dataSocket = socket(AF_INET, SOCK_STREAM)
    dataSocket.connect((serverName, dataPort))
    # wait for server to send requested list of files
    list_of_files = dataSocket.recv(1024).decode()
    dataSocket.close()
    return list_of_files

# -----main-------------------

# establish connection
establish_control_connection();

keep_open = True
status = ''
while keep_open:
    userInput = input("ftp> ")
    user = userInput.split(" ")
    if user[0] == 'quit':
        keep_open = False
    elif user[0] == 'get':
        filename = user[1]

        # send 'get' and file name to the server
        controlSocket.send(userInput.encode())

        # server responds with the new data port
        dataPort = int(controlSocket.recv(1024).decode())

        # Connect to Data Socket on server
        dataSocket = socket(AF_INET, SOCK_STREAM)
        dataSocket.connect((serverName, dataPort))

        # Receiving requested file's size
        fileSizeBuff = recFile(dataSocket,10)
        fileSize = int(fileSizeBuff)

        # -1 indicates the file does not exist
        if fileSize != -1:
            #receive file
            fileData = recFile(dataSocket, fileSize)

            #save file in local storage
            mkFile(filename, fileData)
            status = '200OK'
        else:
            status_json = controlSocket.recv(1024).decode()
            status = json.loads(status_json)['status_code']
        dataSocket.close()

    elif user[0] == 'put':
        filename = user[1]
        # print(filename)
        fileinfo = getFileInfo(filename)
        if(fileinfo == -1):
            print("cannot find file \'{}\'".format(filename))
        else:
            controlSocket.send(userInput.encode())
            dataPort = int(controlSocket.recv(1024).decode())
            dataSocket = socket(AF_INET, SOCK_STREAM)
            dataSocket.connect((serverName, dataPort))
            numBytes = 0
            while len(fileinfo) > numBytes:
                numBytes += dataSocket.send(fileinfo[numBytes].encode())
            status = controlSocket.recv(1024).decode()
            dataSocket.close()

    elif user[0] == 'ls':
        files = get_list_files()
        print(files)
        status = controlSocket.recv(1024).decode()

    print(status)

controlSocket.close()
