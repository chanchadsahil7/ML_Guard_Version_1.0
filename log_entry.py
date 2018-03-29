import MySQLdb
from datetime import datetime
from PIL import Image
import StringIO
import cv2
import base64

def get_connection():
    conn = MySQLdb.connect(host="mlcharts.chmlicpo0yn5.us-east-2.rds.amazonaws.com",
                           port=3306,
                           user="solivarlabs",
                           passwd="solivarlabs",
                           db="mlcharts")
    # conn = MySQLdb.connect(host="localhost",
    #                        user="root",
    #                        passwd="raviprince57",
    #                        db="mlcharts")
    return conn

def log(filename):
    user_registration_id = 3
    conn = get_connection()
    cur = conn.cursor()
    try:
        blob = open(filename,'rb').read()
        encoded_blob = base64.b64encode(blob)
        in_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("INSERT INTO cars_log(license_plate,in_time,car_image,cid) VALUES (%s,%s,%s,%s)",
                    ('0',in_time,encoded_blob,user_registration_id))
        conn.commit()
        print("Logged successfully")
        # cur.execute("SELECT car_image from cars_log ORDER BY id DESC LIMIT 1")
        # data = cur.fetchall()
        # img = data[0][0]
        # img = base64.b64decode(img)
        # file_like = StringIO.StringIO(img)
        # img = Image.open(file_like)
        # img.save("retrieved_image.png")
    except Exception as e:
        print("Exception is ", e)
        conn.rollback()
    conn.close()
    return

if __name__ == "__main__":
    filename = input('Enter the path of the file : ')
    log(filename)