import time  
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler 
import sys
import telepot
from telepot.loop import MessageLoop
import os
import requests

bot = telepot.Bot('514668041:AAGf5C4tA9qMSjUoXfPUbJdo1mRgNzj_-7Q')
url = "https://api.telegram.org/bot514668041:AAGf5C4tA9qMSjUoXfPUbJdo1mRgNzj_-7Q/sendPhoto";

def sendImage(filename):
    files = {'photo': open(filename, 'rb')}
    data = {'chat_id' : "461262677"}
    text_data = "Person Detected"
    bot.sendMessage(data['chat_id'], text=text_data)
    r= requests.post(url, files=files, data=data)

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
        print("created")
        sendImage(event.src_path)
        print("Message Sent")
        print(event.src_path, event.event_type)  # print now only for degug

    def on_created(self, event):
        self.process(event)

if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else 'images/')
    observer.start()

    try:
        while True:
            #bot.polling(none_stop=True)
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()