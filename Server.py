#server code
from socket import *
import sys
from os import listdir

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

#Generate and open data connection
def generate_ephemeral_port(connectionSocket):
    dataSocket = socket(AF_INET, SOCK_STREAM)
    dataSocket.bind(('',0))

    # Send Data port number back to client
    dataPort = str(dataSocket.getsockname()[1])
    connectionSocket.send(dataPort.encode())
    print("Server chose ephemeral port: ", dataPort)

    # store client token
    userPort[data] = dataPort;

    dataSocket.listen(1);
    dataConnection, addr = dataSocket.accept()
    return dataConnection

def list_files():
   # connectionSocket, addr = dataPort.accept()
    fileList = listdir('./userFiles')
    files= " "
    return files.join(fileList)

def send_data(socket,data):
    socket.send(data.encode())


#Establish Control Connection
connectionSocket, addr = serverSocket.accept()
data = connectionSocket.recv(1024).decode()
print('client token: ' + data)
status = '200OK'
send_data(connectionSocket,status)

#forever accept incoming connections
while 1:
    msg = connectionSocket.recv(1024).decode()
    if msg == 'ls':
        print('Listing all files')
        dataConnection = generate_ephemeral_port(connectionSocket)
        files = list_files()
        dataConnection.send(files.encode())
        dataConnection.close()


connectionSocket.close()


# class Datagram:
#     def __init__(self,message):
#         self.message = message
## process message to send back to client
# data = data.replace("client","server")
# obj = Datagram(data.encode())
# data = ""