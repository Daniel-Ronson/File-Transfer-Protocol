#server code
from socket import *
import sys

#user supplied values, command line arguments
try:
    #the port on which to listen
    serverPort=sys.argv[1]

#default port number
except:
    serverPort = 21

#create a TCP socket
serverSocket = socket(AF_INET,SOCK_STREAM)

#bind the connection to the port
serverSocket.bind(('',serverPort))

#start listening for incoming connections
serverSocket.listen(1)
print("The server is ready to recieve on port number: " + str(serverPort) )

#the buffer to store the recieved data
data = ""

#store user access token and associated port number
userPort= {}

def generate_ephemeral_port():
    dataPort = socket(AF_INET, SOCK_STREAM)
    dataPort.bind(('',0))
    return dataPort

class Datagram:
    def __init__(self,message):
        self.message = message

#forever accept incoming connections
#Establish Control Connection
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

        #save cleint data, expecting a unique token
        data += tmpBuff
        #print out what the client sent
        print('client token: ' + data)

        #process message to send back to client
        data = data.replace("client","server")
        obj = Datagram(data.encode())
        data = ""

        #generate ephemeral port
        dataPort = generate_ephemeral_port()
        dataPort_str = str(dataPort.getsockname()[1])

        #store client token
        userPort[data] = dataPort_str;

        print("Server chose ephemeral port: ", dataPort_str)
        connectionSocket.send(dataPort_str.encode())


connectionSocket.close()
