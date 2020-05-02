# server code


from socket import *
import sys
from os import listdir, path

# user supplied values, command line arguments
try:
    # the port on which to listen
    serverPort = int(sys.argv[1])

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
    try:
        dataSocket = socket(AF_INET, SOCK_STREAM)
        dataSocket.bind(('', 0))

        # Send Data port number back to client
        dataPort = str(dataSocket.getsockname()[1])
        connectionSocket.send(dataPort.encode())
        # print("Server chose ephemeral port: ", dataPort)

        # store client token
        userPort[data] = dataPort;

        dataSocket.listen(1);
        dataConnection, addr = dataSocket.accept()
        return dataConnection
    except:
        status = "500InternalServerError"
        print_status(status)


def mkFile(filename, fileData):
    newPath = "./serverStorage/" + cmd[1]
    f = open(newPath, "w+")
    f.write(fileData)
    f.flush()
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

def getFileInfo(filename):
    try:
        path = './serverStorage/' + filename
        fileObj = open(path)
        fileData = fileObj.read(65536)
        filesize = 0
        if fileData:
            filesize = str(len(fileData))
            while len(filesize) < 10:
                filesize = "0" + filesize
                #print(filesize + " the file size")

        fileData = filesize + fileData
        return fileData
    except:
        status = "500InternalServerError"
        print_status(status)


def list_files():
    try:
        fileList = listdir('./serverStorage')
        files = " "
        return files.join(fileList)
    except:
        status = "500InternalServerError"
        print_status(status)


def send_data(socket, data):
    socket.send(data.encode())


def testcase():
    print("works")

def print_status(status):
    if status=='200OK':
        print("SUCCESS. \n");
    else:
        print("FAILURE. \n");


# Establish Control Connection
connectionSocket, addr = serverSocket.accept()
data = connectionSocket.recv(1024).decode()
# print('client token: ' + data)
status = '200OK'
print_status(status);
send_data(connectionSocket, data)

# forever accept incoming connections
while 1:
    msg = connectionSocket.recv(1024).decode()
    cmd = msg.split(" ")
    if cmd[0] == 'ls':
        print('Listing all files...')
        dataConnection = generate_ephemeral_port(connectionSocket)
        files = list_files()
        dataConnection.send(files.encode())
        dataConnection.close()
        status = '200OK'
        print_status(status)
    elif cmd[0] == 'put':
        print('Receiving files...')
        dataConnection = generate_ephemeral_port(connectionSocket)
        fileSizeBuff = recFile(dataConnection, 10)
        # print(fileSizeBuff)
        fileSize = int(fileSizeBuff)
        fileData = recFile(dataConnection, fileSize)
        mkFile(cmd[1], fileData)
        dataConnection.close()
        status = '200OK'
        print_status(status)
    elif cmd[0] == 'get':
        fileName = cmd[1]
        print('Sending files...')
        dataConnection = generate_ephemeral_port(connectionSocket)
        fileData = getFileInfo(fileName)
        print('Getting file data...')
		# number of bytes sent
        numSent = 0		

		# send file
        while len(fileData) > numSent:
            try:
                numSent += dataConnection.send(fileData[numSent:].encode())
            except:
                status = '500InternalServerError'
                print_status(status)
        dataConnection.close()        
        status = '200OK'
        print_status(status)
	

connectionSocket.close()

# class Datagram:
#     def __init__(self,message):
#         self.message = message
## process message to send back to client
# data = data.replace("client","server")
# obj = Datagram(data.encode())
# data = ""
