import time,datetime  
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler 
import sys
import telepot
from telepot.loop import MessageLoop
import os
import MySQLdb
import socket
bot = telepot.Bot('514668041:AAGf5C4tA9qMSjUoXfPUbJdo1mRgNzj_-7Q')

def sendImage(filename):
                     # Import socket module
    s = socket.socket()             # Create a socket object
    host = '107.180.71.58'     # Get local machine name
    port = 8000                    # Reserve a port for your service.
    #s.bind((host, port))
    s.connect((host, port))
    s.send("Hello Sever")

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

    #f.close()
    print('Successfully sent the file')
    s.close()
    print('connection closed')
    

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.jpg", "*.jpeg", "*.png"]

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        #print("created")
        #sendImage(event.src_path)
        print("Message Sent")
        print(event.src_path, event.event_type)  # print now only for degug
        filename=event.src_path
        blob_value = open(filename,'rb').read()
        sendImage(blob_value)
        #i=i+1

    def on_created(self, event):
        self.process(event)

if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else 'images/')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
