import time,datetime  
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler 
import sys
import telepot
from telepot.loop import MessageLoop
import os
import MySQLdb

bot = telepot.Bot('514668041:AAGf5C4tA9qMSjUoXfPUbJdo1mRgNzj_-7Q')

def sendImage(filename):
    url = "https://api.telegram.org/bot514668041:AAGf5C4tA9qMSjUoXfPUbJdo1mRgNzj_-7Q/sendPhoto";
    files = {'photo': open(filename, 'rb')}
    data = {'chat_id' : "461262677"}
    text_data = "Person Detected"
    bot.sendMessage(data['chat_id'], text=text_data)

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
        in_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = MySQLdb.connect(host="mlcharts.chmlicpo0yn5.us-east-2.rds.amazonaws.com",
                  port=3306,
                  user="solivarlabs",
                  passwd="solivarlabs",
                  db="mlcharts")
        cur=conn.cursor()
        cur.execute("""INSERT INTO faces_log(face_image,in_time,cid,name) VALUES (%s,%s,%s,%s)""",(blob_value,in_time,2,'UNKNOWN'))
        conn.commit()
        print("Logged Successfully")
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