import os
import sys
import time

import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber, MessageSubscriber

import struct
from datetime import datetime, timedelta, time
import cv2
import numpy as np

import build.webcam_pb2 as webcam_pb2

got_frame = False
deserialized_x = None


def callbackWebcam(topic_name, msg, time): # msg = webcam_pb2.webcam_raw
    global got_frame
    global deserialized_x
    # part 2: read and visualize -> 2do: push to subscriber node
    deserialized_bytes = np.frombuffer(msg.payload, dtype=np.uint8)
    print("webcam msg received. size = ", deserialized_bytes.size)
    deserialized_x = np.reshape(deserialized_bytes, newshape=(512, 512, 4))
    got_frame = True


def main():
    global got_frame
    # initialize the camera
    # If you have multiple camera connected with
    # current device, assign a value in cam_port
    # variable according to that
    cam_port = 1

    # option1 - show
    cam = cv2.VideoCapture(cam_port)

    # print eCAL version and date
    print("eCAL {} ({})\n".format(ecal_core.getversion(),ecal_core.getdate()))

    # initialize eCAL API
    ecal_core.initialize(sys.argv, "py_webcam_sub")

    # set process state
    ecal_core.set_process_state(1, 1, "I feel good")

    # create publisher
    subwebcam = ProtoSubscriber("WEBCAM_RAW", webcam_pb2.webcam_raw)
    subwebcam.set_callback(callbackWebcam)
    print("webcam subscriber started")
    print("webcam callback registered")

    cv2.namedWindow("webcam_subscriber", cv2.WINDOW_NORMAL) 
    cv2.resizeWindow("webcam_subscriber", 640, 480) 

    # subscribe to webcam message
    while ecal_core.ok():
        if (got_frame == True):
            cv2.imshow('webcam_subscriber', deserialized_x)
            got_frame = False
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    
    # finalize eCAL API
    ecal_core.finalize()

if __name__ == "__main__":
    main()