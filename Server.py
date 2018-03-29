
hostName="mainServer"
hostPort=7734

activePeerList=[]

def main():
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
    
    serversocket.close()
    
if __name__ == '__main__':
    main()    
    
class ActivePeer:
    def __init__(self,hostName='None',uploadPort='None'):
        self.hostname=hostName
        self.uploadPort=uploadPort#port number where upload server of the port is listening.
        
    def __str__(self):
        return 'Hostname is '+str(self.hostname) +' upload port is :'+str(self.uploadPort)
    
class RFC:
    def __init__(self,rfcNumber='None',rfcTitle='None'):
        self.rfcNumber=rfcNumber
        self.rfcTitle=rfcTitle
        self.rfcActivePeer=ActivePeer()
    
    def __str__(self):
        return 'RFC Number is '+str(self.rfcNumber) +' RFC Title is :'+str(self.rfcTitle)+' Active peer hostname is '+str(self.rfcActivePeer.hostname)+' and upload port is :'+str(self.rfcActivePeer.uploadPort)
    
    