# USAGE
# python deep_learning_object_detection.py --image images/example_01.jpg \
#	--prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# import the necessary packages
from log_entry import log
import numpy as np
import argparse
import cv2
import time
import math
import cv2
import dlib
import numpy as np
import MySQLdb
import datetime
import argparse
import time
import telepot
from telepot.loop import MessageLoop
import requests

bot = telepot.Bot('514668041:AAGf5C4tA9qMSjUoXfPUbJdo1mRgNzj_-7Q')

def sendImage(filename):
    url = "https://api.telegram.org/bot514668041:AAGf5C4tA9qMSjUoXfPUbJdo1mRgNzj_-7Q/sendPhoto";
    files = {'photo': open(filename, 'rb')}
    data = {'chat_id' : "461262677"}
    text_data = "Person Detected"
    bot.sendMessage(data['chat_id'], text=text_data)
    r= requests.post(url, files=files, data=data)
    
val=0
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=False,
# 	help="path to input image")
# ap.add_argument("-p", "--prototxt", required=True,
# 	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-cam", "--camera", required=False, default= 'cv2',
	help="to run which camera")
# ap.add_argument("-m", "--model", required=True,
# 	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.7,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("prototxt.txt", "model")

# load the input image and construct an input blob for the image
# by resizing to a fixed 300x300 pixels and then normalizing it
# (note: normalization is done via the authors of the MobileNet SSD
# implementation)

def pi_video_capturing():
    import picamera
    from picamera.array import PiRGBArray
    camera = picamera.PiCamera()
    camera.resolution = (1280, 720)
    camera.framerate = 30
    cap = PiRGBArray(camera, size=(1280, 720))
    camera.start_preview()
    j=0
    flag = False
    con2 = 0
    while True:
        try:
            #print("Entered")
            image = 0
            frame = 0
            detections=0
            frame  = next(camera.capture_continuous(cap, format="bgr", use_video_port=True))
            #frame = camera.capture(cap,format="bgr",use_video_port=True)
            image = frame.array
            #print(frame,image)
            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

            # pass the blob through the network and obtain the detections and
            # predictions
            print("[INFO] computing object detectionss...")
            net.setInput(blob)
            detections = net.forward()

            # loop over the detections
            for i in np.arange(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence > 0.95 and con2 != confidence:
                    con2 = confidence                 # extract the index of the class label from the `detections`,
                    # then compute the (x, y)-coordinates of the bounding box for
                    # the object
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    # display the prediction
                    label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                    diagonal = math.sqrt((endY-startY)**2 + (endX-startX)**2)
                    print(diagonal,CLASSES[idx])
                    if CLASSES[idx]=="person":
                        car_image_name = "images/result"+str(j)+".png"
                        cv2.rectangle(image, (startX, startY), (endX, endY),
                        COLORS[idx], 2)
                        j+=1
                        cv2.imwrite(car_image_name, image)
                        #sendImage(car_image_name)
                        print("[INFO] {}".format(label))
                        #log("result.png")
                        y = startY - 15 if startY - 15 > 15 else startY + 15
                        cv2.putText(image, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                        break
                    else:
                        break
                
            # show the output image
            cap.truncate(0)
            #cv2.imshow("Output", image)
        except KeyboardInterrupt as e:
            camera.close()
            print(e)

def cv2_video_capturing():
    cap = cv2.VideoCapture(0)
    j=0
    while True:
        ret, image = cap.read()
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (480.480)), 0.007843, (480,480), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        print("[INFO] computing object detectionss...")
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > args["confidence"]:
                # extract the index of the class label from the `detections`,
                # then compute the (x, y)-coordinates of the bounding box for
                # the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # display the prediction
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                diagonal = math.sqrt((endY-startY)**2 + (endX-startX)**2)
                print(diagonal,CLASSES[idx])
                if CLASSES[idx]=="person" :
                    #time.sleep(5)
                    car_image_name = "images/result"+str(j)+".png"
                    j+=1
                    cv2.rectangle(image, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                    cv2.imwrite(car_image_name, image)
                    print("[INFO] {}".format(label))
                    #log("result.png")
                    print("breaking")
                    break
                
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(image, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

        # show the output image
        cv2.imshow("Output", image)
        if cv2.waitKey(33)==27:
            break

if __name__ == "__main__":
    if args['camera'] == 'pi':
        pi_video_capturing()
    else:
        cv2_video_capturing()