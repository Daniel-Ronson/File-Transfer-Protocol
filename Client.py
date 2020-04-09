from socket import *

serverName = "localhost"
serverPort = 12000

clientSocket = socket(AF_INET,SOCK_STREAM)

clientSocket.connect((serverName,serverPort))

data = 'This is data from the client which is not very long and over 40 bytes'
bytesSent = 0

while bytesSent != len(data):

    bytesSent += clientSocket.send(data.encode()[bytesSent:])

    #recieve response from server
    newSentence = clientSocket.recv(1024)

print(newSentence.decode())
clientSocket.close()
