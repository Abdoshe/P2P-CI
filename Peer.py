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
    
    
def peer_download(downloadSocket, rfcNumber,hostName):
    if rfcNumber is not None:
        rfcNumber = raw_input('Enter the RFC number to be downloaded: ')
        message = 'GET RFC ' + rfcnumber + ' P2P-CI/1.0\nHost: ' + str(hostname) + '\nOS: ' + platform.system() + ' ' + platform.release()
    downloadsocket.send(message)
    data = downloadsocket.recv(1024)
    data = downloadsocket.recv(1024)
    while data:
        print data
        data = downloadsocket.recv(1024)
    downloadsocket.close()
    #print 'Enter your choice:'
    return 0
    