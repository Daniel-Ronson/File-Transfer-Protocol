from socket import *
import sys
import json

#user supplied values, command line arguments
try:
    serverName = sys.argv[1]
    serverPort = sys.argv[2]

#default values
except:
    serverName = "localhost"
    serverPort = 12000

clientSocket = socket(AF_INET,SOCK_STREAM)

clientSocket.connect((serverName,serverPort))

data = 'connected from client'

def connect_to_server():
    bytesSent = 0
    while bytesSent != len(data):

        bytesSent += clientSocket.send(data.encode()[bytesSent:])

        #recieve response from server
        dataGramBytes = clientSocket.recv(1024)
        dataGram = dataGramBytes.decode()
        dataGram = json.loads(dataGram)
    print("Data port connection at: " + dataGram['socketNumber'] + " " + dataGram['status'])

keep_open = True
while keep_open:
    #userInput = input("ftp>")
    connect_to_server()
    keep_open = False if input("Close Connection? y or n: ") == 'y' else True

clientSocket.close()
