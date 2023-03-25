import cv2
import mediapipe as mp
import time
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# For static images:
# IMAGE_FILES = []
# with mp_face_detection.FaceDetection(
#     model_selection=1, min_detection_confidence=0.5) as face_detection:
#   for idx, file in enumerate(IMAGE_FILES):
#     image = cv2.imread(file)
#     # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
#     results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     # Draw face detections of each face.
#     if not results.detections:
#       continue
#     annotated_image = image.copy()
#     for detection in results.detections:
#       print('Nose tip:')
#       print(mp_face_detection.get_key_point(
#           detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
#       mp_drawing.draw_detection(annotated_image, detection)
#     cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)

# For webcam input:
# cap = cv2.VideoCapture('http://192.168.100.147:81/stream')
class LoadBar():
  def __init__(self):
    self.count = 0
    self.count_min = 0
    self.count_max = 1
    self.count_step = 0.02
    self.load_bar_relative_height = 0.1
  
  def draw_load_bar_base(self, img, detection):
    location = detection.location_data
    relative_bounding_box = location.relative_bounding_box
    if not location.HasField('relative_bounding_box'):
      return
    image_rows, image_cols, _ = image.shape
    rectangle_height = self.load_bar_relative_height*relative_bounding_box.height
    top_left_x = relative_bounding_box.xmin
    top_left_y = relative_bounding_box.ymin - rectangle_height
    top_left = mp_drawing._normalized_to_pixel_coordinates(top_left_x, top_left_y, image_cols, image_rows)
    bottom_right_x = relative_bounding_box.xmin + relative_bounding_box.width
    bottom_right_y = relative_bounding_box.ymin
    bottom_right = mp_drawing._normalized_to_pixel_coordinates(bottom_right_x, bottom_right_y, image_cols, image_rows)
    cv2.rectangle(img, top_left, bottom_right, (128, 128, 128), -1)

  def draw_loading(self, img, detection):
    location = detection.location_data
    relative_bounding_box = location.relative_bounding_box
    image_rows, image_cols, _ = image.shape
    rectangle_height = self.load_bar_relative_height*relative_bounding_box.height
    top_left_x = relative_bounding_box.xmin + relative_bounding_box.width
    top_left_y = relative_bounding_box.ymin - rectangle_height
    top_left = mp_drawing._normalized_to_pixel_coordinates(top_left_x, top_left_y, image_cols, image_rows)
    bottom_right_x = relative_bounding_box.xmin + relative_bounding_box.width * ( 1 - self.count)
    bottom_right_y = relative_bounding_box.ymin
    bottom_right = mp_drawing._normalized_to_pixel_coordinates(bottom_right_x, bottom_right_y, image_cols, image_rows)
    cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), -1)
  
  def reset_load_bar(self):
    self.count = self.count_min

  def draw_load_bar(self, img, detection):
    if self.count < self.count_max:
      self.count += self.count_step
    self.draw_load_bar_base(img, detection)
    self.draw_loading(img, detection)
    return True if self.count >= self.count_max else False

    

cap = cv2.VideoCapture(0)
load_bar = LoadBar()
with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.7) as face_detection:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image)

    # Draw the face detection annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.detections:
      if len(results.detections) == 1:
        detection = results.detections[0]
        loaded = load_bar.draw_load_bar(image, detection)
        mp_drawing.draw_detection(image, detection)
        if loaded:
          time.sleep(5)
          load_bar.reset_load_bar()
      else:
        load_bar.reset_load_bar()
        for detection in results.detections:
          mp_drawing.draw_detection(image, detection)
    else:
      load_bar.reset_load_bar()
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()


# # cap1 = cv2.VideoCapture('http://192.168.100.146:81/stream')
# # cap2 = cv2.VideoCapture('http://192.168.100.147:81/stream')
# cap1 = cv2.VideoCapture(0)
# cap2 = cv2.VideoCapture(2)
# with mp_face_detection.FaceDetection(
#     model_selection=0, min_detection_confidence=0.5) as face_detection:
#   while cap1.isOpened() and cap2.isOpened():
#     success1, image1 = cap1.read()
#     success2, image2 = cap2.read()
#     if not success1:
#       print("Ignoring empty camera1 frame.")
#       # If loading a video, use 'break' instead of 'continue'.
#       cap1.release()
#       cap2.release() 
#       cap1 = cv2.VideoCapture('http://192.168.100.146:81/stream')
#       cap2 = cv2.VideoCapture('http://192.168.100.147:81/stream')
#       continue
#     if not success2:
#       print("Ignoring empty camera2 frame.")
#       # If loading a video, use 'break' instead of 'continue'.
#       cap1.release()
#       cap2.release() 
#       cap1 = cv2.VideoCapture('http://192.168.100.146:81/stream')
#       cap2 = cv2.VideoCapture('http://192.168.100.147:81/stream')
#       continue

#     # To improve performance, optionally mark the image as not writeable to
#     # pass by reference.
#     image1.flags.writeable = False
#     image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
#     results = face_detection.process(image1)

#     # Draw the face detection annotations on the image.
#     image1.flags.writeable = True
#     image1 = cv2.cvtColor(image1, cv2.COLOR_RGB2BGR)
#     if results.detections:
#       for detection in results.detections:
#         if detection.location_data.relative_bounding_box.height > 0.3:
#           print(detection.location_data.relative_bounding_box.height)
#           mp_drawing.draw_detection(image1, detection)
#     # Flip the image horizontally for a selfie-view display.
#     cv2.imshow('MediaPipe Face Detection1', cv2.flip(image1, 1))

#     # To improve performance, optionally mark the image as not writeable to
#     # pass by reference.
#     image2.flags.writeable = False
#     image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
#     results = face_detection.process(image2)

#     # Draw the face detection annotations on the image.
#     image2.flags.writeable = True
#     image2 = cv2.cvtColor(image2, cv2.COLOR_RGB2BGR)
#     if results.detections:
#       for detection in results.detections:
#         mp_drawing.draw_detection(image2, detection)
#     # Flip the image horizontally for a selfie-view display.
#     cv2.imshow('MediaPipe Face Detection2', cv2.flip(image2, 1))
#     if cv2.waitKey(5) & 0xFF == 27:
#       break
# cap1.release()
# cap2.release()
