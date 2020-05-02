## How to Run
  ###python Server.py <Server-Port>
  ###python Client.py <Server-IP> <Server-Port>
  Client will be prompted with ftp> and may input one command
  ###ftp> get | post | ls | quit

## FTP Specification
 - Parallel control and data connections
 - Client initiates control connection on server port number 21 by sending authentication token
 - Server stores auth token to track the session
 - Server creates ephemeral port number for data connection with client session
 - Client can use commands on the server.. get, post, ls, quit
 - Data connection is used to transfer one file, then it closes
 
## Get
 1. Client send get method over control connection
 2. Server responds with file contents, 200OK 
 3. Server closes connection
 - GET datagram contains the name of file, GET header, and user token
 
## Post:
 1. Client intitates post over control connection
 2. Server responds with ephemeral port number for data connection
 3. Client sends file
 4. Server receives file, notifies client with 200OK
 5. Server closes connection.
 - POST datagram contains file contentts, post header, and user token