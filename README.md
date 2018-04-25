# Peer to peer with Centralized Index.
Name: Himani(hhimani)
Name Pavneet Singh Anand(panand4)

I Steps to run the server side 


1) Run the Server: $python Server.py (We have used python version 2.7) 

II Steps to run the Peer side 
1) Run peer on one of the peer $python Peer.py 
Multiple ports can support different peers.
It asks for the following details:

Enter the upload port - 8282 (you can enter the port you wish to run your peer's upload service on)
Enter the server IP (IP address of the server)

Here are a list of options that come up for a Peer.

'************Select option*******************'<br>
    print '1. Add RFC'<br>
    print '2. List RFCs'<br>
    print '3. Lookup RFC'<br>
    print '4. Download RFC'<br>
    print '5. Exit( Press Ctrl+Z after getting OK status)'<br>

III Steps for Peer-to-Peer Application 
1) Copy all the rfcs(that you you want to make available as a peer server)and Peer.py in a single 
folder and run the centralized server on some other machine. 
2) By Default we have added 1 rfc. Its name is RFC123 and the name is IP.
So please have it in your working folder before you start the client code.

1) Rename the RFC in the following format within the folder containing the Peer.py python file as : RFC<number>.txt , For example: RFC123.txt

Option 1 Add RFC
The following details are required (taken with RFC123.txt)
Enter the RFC number: RFC123
Enter the RFC title : A Proferred Official ICP
