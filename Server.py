# server code


from socket import *
import sys
from os import listdir, path

# user supplied values, command line arguments
try:
    # the port on which to listen
    serverPort = sys.argv[1]

# default port number
except:
    serverPort = 21

# create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# bind the connection to the port
serverSocket.bind(('', serverPort))

# start listening for incoming connections
serverSocket.listen(1)
print("The server is ready to recieve on port number: " + str(serverPort))

# the buffer to store the recieved data
data = ""

# store user access token and associated port number
userPort = {}


# Generate and open data connection
def generate_ephemeral_port(connectionSocket):
    dataSocket = socket(AF_INET, SOCK_STREAM)
    dataSocket.bind(('', 0))

    # Send Data port number back to client
    dataPort = str(dataSocket.getsockname()[1])
    connectionSocket.send(dataPort.encode())
    print("Server chose ephemeral port: ", dataPort)

    # store client token
    userPort[data] = dataPort;

    dataSocket.listen(1);
    dataConnection, addr = dataSocket.accept()
    return dataConnection


def mkFile(filename, fileData):
    newPath = "C:/Users/abidb/Documents/File-Transfer-Protocol/File-Transfer-Protocol/userFiles/" + cmd[1]
    f = open(newPath, "w+")
    f.write(fileData)
    f.close()


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


def list_files():
    # connectionSocket, addr = dataPort.accept()
    fileList = listdir('./userFiles')
    files = " "
    return files.join(fileList)


def send_data(socket, data):
    socket.send(data.encode())


def testcase():
    print("works")


# Establish Control Connection
connectionSocket, addr = serverSocket.accept()
data = connectionSocket.recv(1024).decode()
print('client token: ' + data)
status = '200OK'
send_data(connectionSocket, status)

# forever accept incoming connections
while 1:
    msg = connectionSocket.recv(1024).decode()
    cmd = msg.split(" ")
    if cmd[0] == 'ls':
        print('Listing all files')
        dataConnection = generate_ephemeral_port(connectionSocket)
        files = list_files()
        dataConnection.send(files.encode())
        dataConnection.close()
        testcase()
    elif cmd[0] == 'put':
        print('Receiving files')
        dataConnection = generate_ephemeral_port(connectionSocket)
        fileSizeBuff = recFile(dataConnection, 10)
        print(fileSizeBuff)
        fileSize = int(fileSizeBuff)
        fileData = recFile(dataConnection, fileSize)
        mkFile(cmd[1], fileData)
        break
    elif cmd[0] == 'get':
        print('Sending files')
        dataConnection = generate_ephemeral_port(connectionSocket)

        fileNameSize = recvAll(newSock, 10)
        fileName = recvAll(newSock, int(fileNameSize))
        # print('file name : ' + fileName + '\n')

        fileObj = open(fileName, "r")

        # Read 65536 bytes of data
        fileData = fileObj.read(65536)

        # Make sure we did not hit EOF
        if fileData:

		    # Get the size of the data read
		    # and convert it to string
            dataSizeStr = str(len(fileData))

		    # Prepend 0's to the size string
		    # until the size is 10 bytes
            while len(dataSizeStr) < 10:
                dataSizeStr = "0" + dataSizeStr

		    # Prepend the size of the data to the
		    # file data.
            fileData = dataSizeStr + fileData	

		    # number of bytes sent
            numSent = 0		

		    # send file
            while len(fileData) > numSent:
                numSent += newSock.send(fileData[numSent:])

	    # The file has been read. We are done
        else:
            print('FAILURE')
            fileObj.close()
            newSock.close()
            exit()		

connectionSocket.close()

# class Datagram:
#     def __init__(self,message):
#         self.message = message
## process message to send back to client
# data = data.replace("client","server")
# obj = Datagram(data.encode())
# data = ""
