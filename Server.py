#server code
from socket import *
import sys
import json

#user supplied values, command line arguments
try:
    #the port on which to listen
    serverPort=sys.argv[1]

#default port number
except:
    serverPort = 12000

#create a TCP socket
serverSocket = socket(AF_INET,SOCK_STREAM)

#bind the connection to the port
serverSocket.bind(('',serverPort))

#start listening for incoming connections
serverSocket.listen(1)
print("The server is ready to recieve on port number: " + str(serverPort) )

#the buffer to store the recieved data
data = ""


def generate_ephemeral_port():
    dataPort = socket(AF_INET, SOCK_STREAM)
    dataPort.bind(('',0))
    return dataPort

class Datagram:
    def __init__(self,message):
        self.message = message

#forever accept incoming connections
while 1:
    connectionSocket, addr = serverSocket.accept()

    #temporary buffer
    tmpBuff=""
    while len(data) != 1024:
        #receive whatever the newly connected client has to send
        tmpBuff = connectionSocket.recv(1024).decode()
        # The other side unexpectedly closed it's socket
        if not tmpBuff:
            break

        #save data
        data += tmpBuff
        print(data)

        #process message to send back to client
        data = data.replace("client","server")

        #generate ephemeral port
        dataPort = generate_ephemeral_port()
        print("I chose ephemeral port: ", dataPort.getsockname()[1])
        dataPort_str = str(dataPort.getsockname()[1])
        dataGram = {'message':data,'socketNumber':dataPort_str,'status':'200 OK'}
        dataGram = json.dumps(dataGram)
        connectionSocket.send(dataGram.encode())
        data = ""


connectionSocket.close()
