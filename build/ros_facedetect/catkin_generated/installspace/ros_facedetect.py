#!/usr/bin/env python2
# -*- encoding: UTF-8 -*-

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os


def face_detect():
    pub = rospy.Publisher('facedetect', Image, queue_size=10)
    rospy.init_node('facedetect', anonymous=True)
    rate = rospy.Rate(10)  # 10hz

    # Load the Haar cascade file for face detection
    model_path = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_alt.xml')
    face_cascade = cv2.CascadeClassifier(model_path)

    # Create a VideoCapture object to capture video from the default camera
    cap = cv2.VideoCapture(0)

    bridge = CvBridge()

    while not rospy.is_shutdown():
        # Read the current frame from the camera
        ret, frame = cap.read()

        if not ret:
            break

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Perform face detection
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        if len(faces) > 0:
            rospy.loginfo('Face detected: %s' % str(faces))
            # Convert the frame to ROS Image message
            img_msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            pub.publish(img_msg)

        rate.sleep()

    # Release the VideoCapture object and close any open windows
    cap.release()


if __name__ == '__main__':
    try:
        face_detect()
    except rospy.ROSInterruptException:
        pass
