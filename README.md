# Peer to peer with Centralized Index.
Name: Himani(hhimani)
Name Pavneet Singh Anand(panand4)

I Steps to run the server side 


1) Run the Server on the terminal using the following command: 
$python Server.py (We have used python version 2.7) 

II Steps to run the Peer side 

1) Copy all the rfcs(that you you want to make available as a peer server)and Peer.py in a single 
folder and run the centralized server  on some other machine. 
2) By Default we have added 1 rfc. Its name is RFC123 and the name is IP. 
So please have it in your working folder before you start the client code. 
3) Open the Client terminal using the following command: $python Peer.py 
Here are a list of options that come up for a Peer. you can run multiple Peers on multiple upload ports.
'************Select option*******************'<br>
    print '1. Add RFC'<br>
    print '2. List RFCs'<br>
    print '3. Lookup RFC'<br>
    print '4. Download RFC'<br>
    print '5. Exit( Press Ctrl+Z after getting OK status)'<br>

III Steps for Peer-to-Peer Application 

1) Rename the RFC in the following format within the folder containing the Peer.py python file as : RFC<number>.txt. For example: RFC123.txt. 
