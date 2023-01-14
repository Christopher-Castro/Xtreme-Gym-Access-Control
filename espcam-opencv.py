import cv2
from urllib.request import urlopen
import numpy as np
import os

url = r'http://192.168.100.146/640x480.jpg'

cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(haar_model)

while True:
    img_resp = urlopen(url)
    imgnp = np.asarray(bytearray(img_resp.read()), dtype="uint8")
    img = cv2.imdecode(imgnp, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2) 
    cv2.imshow("Camera", img)
    if cv2.waitKey(1) == 113:
        break

# import cv2
# from urllib.request import urlopen
# import numpy as np
# import os
 
# cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
# haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
# face_cascade = cv2.CascadeClassifier(haar_model)

# stream = urlopen('http://192.168.100.146:81/stream')
# bytes = bytes()
# while True:
#     bytes += stream.read(1024)
#     a = bytes.find(b'\xff\xd8')
#     b = bytes.find(b'\xff\xd9')
#     if a != -1 and b != -1:
#         jpg = bytes[a:b+2]
#         bytes = bytes[b+2:]
#         if jpg :
#             img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
#             # Convert to grayscale
#             # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             # # Detect the faces
#             # faces = face_cascade.detectMultiScale(gray, 1.1, 4)
#             # # Draw the rectangle around each face
#             # for (x, y, w, h) in faces:
#             #     cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2) 
#             # Display
#             cv2.imshow('ESP32 CAM', img)
#     if cv2.waitKey(1) & 0xff == ord('q'):
#         break
# stream.release()
# cv2.destroyAllWindows()


# import cv2
# import numpy as np

# import requests

# '''
# INFO SECTION
# - if you want to monitor raw parameters of ESP32CAM, open the browser and go to http://192.168.x.x/status
# - command can be sent through an HTTP get composed in the following way http://192.168.x.x/control?var=VARIABLE_NAME&val=VALUE (check varname and value in status)
# '''

# # ESP32 URL
# URL = "http://192.168.100.146"
# AWB = True

# # Face recognition and opencv setup
# cap = cv2.VideoCapture(URL + ":81/stream")
# face_classifier = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml') # insert the full path to haarcascade file if you encounter any problem

# def set_resolution(url: str, index: int=1, verbose: bool=False):
#     try:
#         if verbose:
#             resolutions = "10: UXGA(1600x1200)\n9: SXGA(1280x1024)\n8: XGA(1024x768)\n7: SVGA(800x600)\n6: VGA(640x480)\n5: CIF(400x296)\n4: QVGA(320x240)\n3: HQVGA(240x176)\n0: QQVGA(160x120)"
#             print("available resolutions\n{}".format(resolutions))

#         if index in [10, 9, 8, 7, 6, 5, 4, 3, 0]:
#             requests.get(url + "/control?var=framesize&val={}".format(index))
#         else:
#             print("Wrong index")
#     except:
#         print("SET_RESOLUTION: something went wrong")

# def set_quality(url: str, value: int=1, verbose: bool=False):
#     try:
#         if value >= 10 and value <=63:
#             requests.get(url + "/control?var=quality&val={}".format(value))
#     except:
#         print("SET_QUALITY: something went wrong")

# def set_awb(url: str, awb: int=1):
#     try:
#         awb = not awb
#         requests.get(url + "/control?var=awb&val={}".format(1 if awb else 0))
#     except:
#         print("SET_QUALITY: something went wrong")
#     return awb

# if __name__ == '__main__':
#     set_resolution(URL, index=8)

#     while True:
#         if cap.isOpened():
#             ret, frame = cap.read()

#             if ret:
#                 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#                 gray = cv2.equalizeHist(gray)

#                 faces = face_classifier.detectMultiScale(gray)
#                 for (x, y, w, h) in faces:
#                     center = (x + w//2, y + h//2)
#                     frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 4)

#             cv2.imshow("frame", frame)

#             key = cv2.waitKey(1)

#             if key == ord('r'):
#                 idx = int(input("Select resolution index: "))
#                 set_resolution(URL, index=idx, verbose=True)

#             elif key == ord('q'):
#                 val = int(input("Set quality (10 - 63): "))
#                 set_quality(URL, value=val)

#             elif key == ord('a'):
#                 AWB = set_awb(URL, AWB)

#             elif key == 27:
#                 break

#     cv2.destroyAllWindows()
#     cap.release()