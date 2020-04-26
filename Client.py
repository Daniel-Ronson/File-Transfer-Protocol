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
def connect_to_server():
    bytesSent = 0
    while bytesSent != len(userToken):

        bytesSent += controlSocket.send(userToken.encode()[bytesSent:])

        #recieve response from server
        dataPort = controlSocket.recv(1024)

    print("Data port connection at: ", dataPort.decode())

#-----main-------------------

#establish connection
connect_to_server();

keep_open = True
while keep_open:
    userInput = input("ftp>")
    if userInput == 'quit':
        keep_open = False
        break;
    if userInput== 'get':
        break;
        # dataSocket = socket(AF_INET, SOCK_STREAM)
        # dataSocket.connect((serverName, dataPort))
        # filename = 'myFile'
        # dataSocket.send(filename.encode())
        # statusCode = dataSocket.recv(1024);
        # print(statusCode)

controlSocket.close()
