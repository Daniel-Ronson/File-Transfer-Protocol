from socket import *
import sys
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

data = 'This is data from the client which is not very long and over 40 bytes'

def send_data():
    bytesSent = 0
    while bytesSent != len(data):

        bytesSent += clientSocket.send(data.encode()[bytesSent:])

        #recieve response from server
        newSentence = clientSocket.recv(1024)

    print(newSentence.decode())

keep_open = True
while keep_open:
    #userInput = input("ftp>")
    send_data()
    keep_open = False if input("Close Connection? y or n: ") == 'y' else True

clientSocket.close()
