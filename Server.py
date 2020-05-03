# server code


from socket import *
import sys
import json
import os

statusOK = '200OK'
statusServerError = '500ServerError'
statusNotFound = '404NotFound'
ABORT = '-1'
def Error(status_code):
    return {'error' : 'error', 'status_code':status_code}

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
        fileSize = os.path.getsize(path)
        fileObj = open(path)
        fileData = fileObj.read(fileSize)
        filesize = 0
        if fileData:
            filesize = str(len(fileData))
            while len(filesize) < 10:
                filesize = "0" + filesize
            #print(filesize + " the file size")

        fileData = filesize + fileData
        return fileData
    except:
        return Error(statusNotFound)

def list_files():
    fileList = os.listdir('./serverStorage')
    files = " "
    return files.join(fileList)


def send_data(socket, data):
    socket.send(data.encode())


def testcase():
    print("works")


# Establish Control Connection
connectionSocket, addr = serverSocket.accept()
try:
    data = connectionSocket.recv(1024).decode()
    print('client token: ' + data)
    send_data(connectionSocket, statusOK)
except:
    send_data(connectionSocket, statusServerError)

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
        connectionSocket.send(statusOK.encode())
    elif cmd[0] == 'put':
        try:
            print('Receiving files')
            dataConnection = generate_ephemeral_port(connectionSocket)
            fileSizeBuff = recFile(dataConnection, 10)
            print(fileSizeBuff)
            fileSize = int(fileSizeBuff)
            fileData = recFile(dataConnection, fileSize)
            mkFile(cmd[1], fileData)
            status = statusOK
        except:
            status = statusServerError
        connectionSocket.send(status.encode())
        dataConnection.close()

    elif cmd[0] == 'get':
        fileName = cmd[1]
        print('Sending files')
        dataConnection = generate_ephemeral_port(connectionSocket)
        fileData = getFileInfo(fileName)

        #type of dict indicates there was an error thrown
        if type(fileData) is dict:
            print(fileData['status_code'])

            #send signal to abort data connection
            dataConnection.send(ABORT.encode())

            #send status code through connection port
            connectionSocket.send(json.dumps(fileData).encode())
        else:
            print('getting file data')
		    # number of bytes sent
            numSent = 0

		    # send file
            while len(fileData) > numSent:
                numSent += dataConnection.send(fileData[numSent:].encode())
        dataConnection.close()
	    

connectionSocket.close()

## process message to send back to client
# data = data.replace("client","server")
# obj = Datagram(data.encode())
# data = ""
