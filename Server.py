
hostName="mainServer"
hostPort=7734
#think do we really need active peers list? if we are storing them in the RFC list? coz that is what we search for

activePeers=[]
activeRFCs=[]

def main():
    serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM) # AF_INET refers to ipv4, SOCK_STREAM refers to implies TCP
    serversocket.connect((hostName, hostPort))
    serversocket.listen(5)## of connection requests it could listen to? shouldn't this number be like 100

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
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.hostName == other.hostName and self.uploadPort == other.uploadPort
        return False
    
class RFC:
    def __init__(self,rfcNumber='None',rfcTitle='None'):
        self.rfcNumber=rfcNumber
        self.rfcTitle=rfcTitle
        self.rfcActivePeer=ActivePeer()
    
    def __str__(self):
        return 'RFC '+str(self.rfcNumber) +' '+str(self.rfcTitle)+' '+str(self.rfcActivePeer.hostname)+' '+str(self.rfcActivePeer.uploadPort)
    
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.rfcNumber == other.rfcNumber and self.rfcTitle == other.rfcTitle and self.rfcActivePeer == other.rfcActivePeer
        return False
    
def peerThreadHandler(peerSocket):
    try:
        while True:
            response=peerSocket.recv(1024)
            if len(response)==0:
                peerSocket.close()
                return
            i=0
            for i in xrange(len(response)):
                if response[i] == '!':
                    break
            #remove after testing
            output = '-----------------------------------------------------------\nThe Client has requested the following:\n'
            new_response = response[:i]
            output = output + response[:i]
            
            split_response=new_response.split();
            if split_response[0]=='ADD':
                addRFC(new_response,peerSocket)
            elif split_response[0]=='LOOKUP':
                lookUpRFC(new_response,peerSocket)
            elif split_response[0]=='LIST':
                listRFC(new_response,peerSocket)
            elif split_response[0]=='DEL':
                deleteRFC(new_response,peerSocket)
    except KeyboardInterrupt:
        serversocket.close()
        sys.exit(0)
        
def concat_message(message):
    finalLength =len(message)
    while finalLength<1024:
        message+='!'
        finalLength+=1
    return message

def addRFC(new_reponse,peerSocket):
    split_response=new_response.split();
    
    rfcNumber = split_response[2]
    hostName = split_response[5]
    uploadPort = split_response[7]
    title1= split_response[9:]
    title = ' '.join(title1)
    #peer is already in the active peer list?
    newPeer=ActivePeer(hostName,uploadPort)
    
    if newPeer not in activePeers:
        activePeers.append(newPeer)
    newRFC=RFC(rfcNumber,title,newPeer)
    if newRFC not in activeRFCs:
        activeRFCs.append(newRFC)
    
    peerMessage = 'RFC '+str(rfcNumber)+' '+str(title1)+' '+str(hostName)+' '+str(uploadPort)
    peerMessage = 'P2P-CI/1.0 200 OK\n' + str(peerMessage)
    peerMessageResponse = concat_message(peerMessage)
    peerSocket.send(peerMessageResponse)
    return 0

def lookUp(new_reponse,peerSocket):
    split_response=new_response.split();
    rfcNumber = split_response[2]
    title1= split_response[9:]
    title = ' '.join(title1)
    count=0
    for activeRFC in activeRFCs:
        if activeRFC.rfcNumber==rfcNumber and activeRFC.rfcTitle==title :
            if count==0:
                message='P2P-CI/1.0 200 OK\n'
            message = message + 'RFC '+str(activeRFC.rfcNumber)+' '+str(activeRFC.rfcTitle)+' '+str(activeRFC.activePeer.hostName)+' '+str(activeRFC.activePeer.uploadPort)
            count+=1;
        if count > 0:
            peerMessageResponse = concat_message(message)
            peerSocket.send(peerMessageResponse)
        if count == 0:
            message = 'P2P-CI/1.0 404 NOT FOUND'
            peerMessageResponse = concat_message(message)
            peerSocket.send(peerMessageResponse)
    
def list(peerSocket):
    code = 0
    status = ''
    rfclist = []
    if len(activeRFCs) == 0:
        message = 'P2P-CI/1.0 404 NOT FOUND'
        peerMessageResponse = concat_message(message)
        peerSocket.send(peerMessageResponse) 
    else:
        counter=0
        message = 'P2P-CI/1.0 200 OK \n'
        for activeRFC in activeRFCs:
           message = message + str(rfc)+ '\n'
           counter+=1
           
        if counter >0 :
            peerMessageResponse = concat_message(message)
            peerSocket.send(peerMessageResponse)
        elif counter ==0:
            message = 'P2P-CI/1.0 404 NOT FOUND'
            peerMessageResponse = concat_message(message)
            peerSocket.send(new_message)
    return 0

def deletePeer(new_response,peerSocket):
    split_response=new_response.split();
    
    hostName = split_response[4]
    uploadPort = split_response[6]
   
    for activeRFC in activeRFCs:
        if activeRFC.activePeer.hostName == hostName and activeRFC.activePeer.uploadPort== uploadPort:
            activeRFCs.remove(activeRFC)
        

    for activePeer in activePeers:
        if activePeer.hostName == hostName and activePeer.uploadPort == uploadPort:
            activePeers.remove(activePeer)

    message = 'P2P-CI/1.0 200 OK \n'
    peerMessageResponse = concat_message(message)
    peerSocket.send(peerMessageResponse)
    