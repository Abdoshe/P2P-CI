
hostName="mainServer"
hostPort=7734

#creating a socket server
#create an INET, STREAMing socket
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM) # AF_INET refers to ipv4, SOCK_STREAM refers to implies TCP
#now connect to the web server on port 80
# - the normal http port
serversocket.connect((hostName, hostPort))
serversocket.listen(5)#At one time it could listen these many connection request? shouldn't this number be like 100

#dispatching thread for each client connection
while 1:
    #accept connections from outside
    (clientsocket, address) = serversocket.accept()
    #now do something with the clientsocket
    #in this case, we'll pretend this is a threaded server
    ct = client_thread(clientsocket)
    ct.run()#run or start?