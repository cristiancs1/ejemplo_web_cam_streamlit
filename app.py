import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from streamlit_webrtc import (
    AudioProcessorBase,
    RTCConfiguration,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class PoseDetector(VideoProcessorBase):
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = None

    def transform(self, frame):
        image = frame.to_ndarray(format="bgr24")

        with self.mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
            results = pose.process(image)
            if results.pose_landmarks is not None:
                self.pose = results.pose_landmarks
                self.mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return image

def app():
    st.title("Demo de pose en tiempo real")
    rtc_configuration = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
    webrtc_ctx = webrtc_streamer(
        key="pose",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=rtc_configuration,
        video_processor_factory=PoseDetector,
        async_processing=True,
    )
    if webrtc_ctx.video_transformer:
        pose = webrtc_ctx.video_transformer.pose
        if pose is not None:
            
            cv2.rectangle(pose, (0,0), (225,73), (245,117,16), -1)
                                    
                                    # Set data
            cv2.putText(pose, 'SET', (15,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 2, cv2.LINE_AA)
            stframe.image(pose,channels = 'BGR',use_column_width=True)
            #st.write(f"Pose: {pose}")

app()