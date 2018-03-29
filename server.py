# server.py
import time,datetime  
import socket
from time import gmtime, strftime# Import socket module

port = 8000                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = '107.180.71.58'     # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(10)                     # Now wait for client connection.
print(socket.gethostname())
print 'Server listening....'

while True:
    conn, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    data = conn.recv(4096)
    print('Server received', repr(data))

    '''filename='my.txt'
    f = open(filename,'rb')
    l = f.read(4096)
    while (l):
       conn.send(l)
       print('Sent ',repr(l))
       l = f.read(4096)
    f.close()'''
    #filename = "images2/" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ".jpg"
    #f = open(filename,'wb')
    #data = s.recv(1024)
    f = open("my.jpg",'wb')
    f.write(data)
    print("File saved")
    f.close()
    conn.send(data)
    print("Sent back")
    #print('Done sending')
    #conn.send('Thank you for connecting')
    conn.close()