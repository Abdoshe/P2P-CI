from socket import *
import os
import threading
import sys
from multiprocessing import Process # Doubt
import time
import platform
import datetime

class ActivePeer:
    def __init__(self,hostname='None',upload_port='None'):
        self.hostname=hostname
        self.upload_port = upload_port
        
    def __str__(self):
        return 'Hostname is '+ str(self.hostname) +' upload port is :' + str(self.upload_port)

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
        return 'RFC ' + str(self.rfc_number) + ' ' + str(self.rfc_title) + ' ' + str(self.rfc_active_peer.hostname) + ' ' + str(self.rfc_active_peer.upload_port)
    
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.rfc_number == other.rfc_number and self.rfc_title == other.rfc_title and self.rfc_active_peer == other.rfc_active_peer
        return False
    
    
def peer_download(peer_socket,rfc_number,hostname):
    if rfc_number is not None:
        msg = 'GET RFC ' + rfc_number + ' P2P-CI/1.0\nHost: ' + str(hostname) + '\nOS: ' + platform.system() + ' ' + platform.release()
    peer_socket.send(msg)
    data = peer_socket.recv(1024)
    filename="RFC"+rfc_number+".txt"
    f= open(filename,"w+")
    while data:
        print data
        f.write(data)
        data = peer_socket.recv(1024)
    f.close()
    peer_socket.close()
    print 'Enter your choice'
    return 0

def peer_server():
    peer_socket = socket(AF_INET,SOCK_STREAM)
    peer_ip = ''
    peer_port = int(upload_port)
    try:
        peer_socket.bind((peer_ip,peer_port))
    except error, msg:
        print 'Binding of socket to given ip, port failed. Error Code: ' + str(msg[0]) + ' Message ' + str(msg[1])
        sys.exit()
    try:
        while True:
            peer_socket.listen(3)
            (conn,socket_info) = peer_socket.accept()
            print '\nConnection initialized on port : ',socket_info[1]
            peer_thread = threading.Thread(target = peer_thread_factory, args = (conn,))
            peer_thread.start()
        peer_socket.close()
    except KeyboardInterrupt:
        peer_socket.close()
        sys.exit(0)

def peer_thread_factory(peer_socket):
    response = peer_socket.recv(1024)
    arr = response.split(' ')
    print arr
    filename = 'RFC' + arr[2] + '.txt'
    print filename
    cwd = os.getcwd()
    files = os.listdir(cwd)
    if filename in files:
        last_modified = time.strftime("%a, %d %b %Y %H:%M:%S ",time.gmtime(os.path.getmtime(filename))) + 'GMT\n'
        OS = platform.system() + ' ' + platform.release()
        curr_time = time.strftime("%a, %d %b %Y %H:%M:%S",time.gmtime()) + 'GMT\n'
        file_size = os.path.getsize(filename)
        msg = 'P2P-CI/1.0 200 OK\nDate: ' + str(curr_time) +'\nOS: ' + str(OS) + '\nLast-Modified: ' + str(last_modified) + '\nContent-Length: ' + str(file_size) + '\nContent-Type: text/text\n'
        peer_socket.send(msg)
        file_handler = open(filename,"r")
        data = file_handler.read(1024)
        while data:
            peer_socket.send(data)
            data = file_handler.read(1024)
        file_handler.close()
    peer_socket.close()
    sys.exit(0)

def add_padding(msg):
    length = len(msg)
    while length < 1024:
        msg += '!'
        length += 1
    return msg

def add_RFC(clientsocket,rfc_number=None,rfc_title=None):
    global hostname
    hostname = gethostname()
    if rfc_title is None:
        rfc_number = raw_input('Enter the RFC number: ')
        rfc_title = raw_input('Enter the RFC title : ')
    msg = 'ADD RFC ' + str(rfc_number) + ' P2P-CI/1.0\nHOST: ' + str(hostname) + '\nPort: ' + str(upload_port) + '\nTitle: ' + str(rfc_title)
    send_receive(msg,clientsocket)

def list_RFC(clientsocket):
    global hostname
    hostname = gethostname()
    msg = 'LIST ALL P2P-CI/1.0\nHOST: ' + str(hostname) + '\nPort: ' + str(upload_port) + '\n'
    send_receive(msg,clientsocket)

def lookup_RFC(clientsocket):
    global hostname
    hostname = gethostname()
    rfc_number = raw_input('Enter the RFC number: ')
    rfc_title = raw_input('Enter the RFC title: ')
    msg = 'LOOKUP RFC ' + str(rfc_number) + ' P2P-CI/1.0\nHost: ' + str(hostname) + '\nPort: ' + str(upload_port) + '\nTitle: ' + str(rfc_title)
    send_receive(msg,clientsocket)

def delete_peer(clientsocket):
    global hostname
    hostname = gethostname()
    msg = 'DEL PEER P2P-CI/1.0\nHOST: ' + str(hostname) + '\nPort: ' + str(upload_port)
    send_receive(msg,clientsocket)

def send_receive(msg,clientsocket):
    msg = add_padding(msg)
    clientsocket.send(msg)
    response = clientsocket.recv(1024)
    i = 0
    for i in xrange(len(response)):
        if response[i] == '!':
              break
    response = response[:i]
    print '\nResponse is\n' + str(response)

def menu():
    print '************Select option*******************'
    print '1. Add RFC'
    print '2. List RFCs'
    print '3. Lookup RFC'
    print '4. Download RFC'
    print '5. Exit( Press Ctrl+Z after getting OK status)'
    return raw_input('Enter your choice:')

def connect_to_server():
    global servername
    serverport = 7734
    servername = raw_input('Enter the server IP: ')
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((servername,serverport))
    #addRFC(client_socket,123,'A Proferred Official ICP')
    while True:
        selection = menu()
        if selection == '1':
            add_RFC(client_socket)
        elif selection == '2':
            list_RFC(client_socket)
        elif selection == '3':
            Lookup_RFC(client_socket)
        elif selection == '4':
            peer_name = raw_input('Enter hostname of peer server: ')
            peer_port = raw_input('Enter upload port of peer: ')
            rfc_num = raw_input('Enter RFC Number')
            peer_socket = socket(AF_INET, SOCK_STREAM)
            peer_socket.connect((peer_name,int(peer_port)))
            peer_download(peer_socket,rfc_num,peer_name)
        elif selection == '5':
            delete_peer(client_socket)
            break
        else:
            print 'Invalid Input'

def main():
    global upload_port
    upload_port = raw_input('Enter the upload port: ')
    try:
        peer_server_thread = threading.Thread(name = 'Peer_server_thread',target = peer_server)
        peer_server_thread.setDaemon(True)
        peer_server_thread.start()
        connect_server_thread = threading.Thread(name = 'server_connect_thread',target = connect_to_server)
        connect_server_thread.setDaemon(True)
        connect_server_thread.start()
        connect_server_thread.join()
        peer_server_thread.join()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()
