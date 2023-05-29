#!/usr/bin/env python2
# -*- encoding: UTF-8 -*-

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

def parse_face_info(data):
    # Split the string by comma to get individual face information
    face_strings = data.split(',')
    parsed_faces = []
    for face_string in face_strings:
        # Remove surrounding brackets
        face_string = face_string.strip('[]')
        # Split the face string by space to get individual values
        face_values = face_string.split()
        # Convert the values to integers
        face = [int(value) for value in face_values]
        parsed_faces.append(face)
    return parsed_faces

def facedetect_callback(data):
    # Convert the ROS Image message to OpenCV format
    bridge = CvBridge()
    try:
        frame = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        rospy.logerr('Error converting ROS Image message to OpenCV format: %s' % str(e))
        return
    
    # Load the Haar cascade file for face detection
    model_path = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_alt.xml')
    face_cascade = cv2.CascadeClassifier(model_path)

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    # Draw red circles around the detected faces
    for (x, y, w, h) in faces:
        center = (x + w // 2, y + h // 2)
        radius = min(w, h) // 2
        cv2.circle(frame, center, radius, (0, 0, 255), 2)

    # Display the image using image_view package
    cv2.imshow("Face Detection", frame)
    cv2.waitKey(1)

def listener():
    rospy.init_node('facedetect_listener_node', anonymous=True)

    rospy.Subscriber('facedetect', Image, facedetect_callback)

    rospy.spin()

if __name__ == '__main__':
    listener()

