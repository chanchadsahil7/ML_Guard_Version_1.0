import socket                   # Import socket module

s = socket.socket()             # Create a socket object
host = '107.180.71.58'     # Get local machine name
port = 8000                    # Reserve a port for your service.
#s.bind((host, port))
s.connect((host, port))
s.send("Hello server!")

'''with open('received_file', 'wb') as f:
    print 'file opened'
    while True:
        print('receiving data...')
        data = s.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        # write data to a file
        f.write(data)'''

f.close()
print('Successfully sent the file')
s.close()
print('connection closed')