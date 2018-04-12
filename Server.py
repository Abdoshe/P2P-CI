from socket import *
import sys
import os
import threading

active_peers=[]
active_RFCs=[]
hostname="centralServer"
port=7734

def main():
    # AF_INET -> ipv4, SOCK_STREAM -> TCP
    server_socket = socket.socket(AF_INET, SOCK_STREAM)
    try:
    	server_socket.bind((hostname,port))
    except error, msg:
		print 'Binding to local address unsuccessful. Error Code: ' + str(msg[0]) + ' Message ' + str(msg[1])
	    sys.exit()
    try:
		while True:
			server_socket.listen(50)
            # Accepting connections
			(conn,socket_info) = server_socket.accept()
            # Spawning thread
			server_thread = threading.Thread(target = peerThreadHandler, args = (conn))
		    server_thread.start()
	except KeyboardInterrupt:
		server_socket.close()
		sys.exit(0)

if __name__ == '__main__':
    main()    
    
class ActivePeer:
    def __init__(self,hostname='None',upload_port='None'):
        self.hostname = hostname
        self.upload_port = upload_port#port number where upload server of the port is listening.
        
    def __str__(self):
        return 'Hostname is ' + str(self.hostname) + ' upload port is :' + str(self.upload_port)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.hostname == other.hostname and self.upload_port == other.upload_port
        return False
    
class RFC:
    def __init__(self,rfc_number='None',rfc_title='None'):
        self.rfc_number = rfc_number
        self.rfc_title = rfc_title
        self.rfc_active_peer = ActivePeer()
    
    def __str__(self):
        return 'RFC '+str(self.rfc_number) +' '+str(self.rfc_title)+' '+str(self.rfc_active_peer.hostname)+' '+str(self.rfc_active_peer.upload_port)
    
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.rfc_number == other.rfc_number and self.rfc_title == other.rfc_title and self.rfc_active_peer == other.rfc_active_peer
        return False
    
def peerThreadHandler(peer_socket):
    try:
        while True:
            response = peer_socket.recv(1024)
            if len(response)==0:
                peer_socket.close()
                return
            i = 0
            for i in xrange(len(response)):
                if response[i] == '!':
                    break
            response = response[:i]
            arr = response.split(' ');
            action = arr[0]
            if action=='ADD':
                addRFC(response,peer_socket)
            elif action=='LOOKUP':
                lookUpRFC(response,peer_socket)
            elif action=='LIST':
                listRFC(response,peer_socket)
            elif action=='DEL':
                deleteRFC(response,peer_socket)
    except KeyboardInterrupt:
        server_socket.close()
        sys.exit(0)
        
def add_padding(msg):
    length = len(msg)
    while length < 1024:
        msg += '!'
        length += 1
    return msg

def addRFC(reponse,peer_socket):
    arr = response.split(' ');
    rfc_number = arr[2]
    hostname = arr[5]
    upload_port = arr[7]
    title = arr[9:]
    title = ' '.join(title)
    #peer is already in the active peer list?
    peer = ActivePeer(hostname,upload_port)
    if peer not in active_peers:
        active_peers.append(peer)
    RFC = RFC(rfc_number,title,peer)
    if RFC not in active_RFCs:
        active_RFCs.append(RFC)
    msg = 'P2P-CI/1.0 200 OK\n' + 'RFC '+str(rfc_number) + ' ' + str(title) + ' '+str(hostname) + ' ' + str(upload_port)
    msg = add_padding(msg)
    peer_socket.send(msg)

def lookUp(response,peer_socket):
    arr = response.split(' ');
    rfc_number = arr[2]
    title = arr[9:]
    title = ' '.join(title)
    count = 0
    msg = 'P2P-CI/1.0 404 NOT FOUND'
    if len(active_RFCs) > 0:
        msg = 'P2P-CI/1.0 200 OK\n'
        for active_RFC in active_RFCs:
            if active_RFC.rfc_number == rfc_number and active_RFC.rfc_title==title :
                msg += 'RFC '+str(active_RFC.rfc_number)+' '+str(active_RFC.rfc_title)+' '+str(active_RFC.active_peer.hostname)+' '+str(active_RFC.active_peer.upload_port)
                count += 1;
    msg = add_padding(msg)
    peer_socket.send(msg)

def list(peer_socket):
    msg = 'P2P-CI/1.0 404 NOT FOUND'
    if len(active_RFCs) > 0:
        count = 0
        msg = 'P2P-CI/1.0 200 OK \n'
        for active_RFC in active_RFCs:
           msg += str(active_RFC)+ '\n'
           count += 1
    msg = add_padding(msg)
    peer_socket.send(msg)

def deletePeer(response,peer_socket):
    arr = response.split(' ');
    hostname = arr[4]
    upload_port = arr[6]
    for active_RFC in active_RFCs:
        if active_RFC.active_peer.hostname == hostname and active_RFC.active_peer.upload_port== upload_port:
            active_RFCs.remove(active_RFC)
    for active_peer in active_peers:
        if active_peer.hostname == hostname and active_peer.upload_port == upload_port:
            active_peers.remove(active_peer)
    msg = 'P2P-CI/1.0 200 OK \n'
    msg = add_padding(msg)
    peer_socket.send(msg)
