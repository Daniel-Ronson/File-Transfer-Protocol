#server code
from socket import *

#the port on which to listen
serverPort=12000

#create a TCP socket
serverSocket = socket(AF_INET,SOCK_STREAM)

#bind the connection to the port
serverSocket.bind(('',serverPort))

#start listening for incoming connections
serverSocket.listen(1)
print("The server is ready to recieve")

#the buffer to store the recieved data
data = ""

#forever accept incoming connections
while 1:
# Accept a connection ; get client ’ s socket
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

        data = data.replace("client","server")
        connectionSocket.send(data.encode())

connectionSocket.close()
