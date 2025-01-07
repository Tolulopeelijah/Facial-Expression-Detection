import streamlit as st
import cv2
import tempfile
from pred_processing import process_video

def record_video():
    """Allows the user to record a video using their webcam."""
    st.title("Record a Video")
    run = st.button("Start Recording")
    stop = st.button("Stop Recording")
    
    if "recording" not in st.session_state:
        st.session_state.recording = False

    if run:
        st.session_state.recording = True
    elif stop:
        st.session_state.recording = False

    # Open webcam stream
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Error accessing webcam.")
        return None

    # Temporary file to save the recording
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    video_writer = None

    while st.session_state.recording:
        ret, frame = cap.read()
        if not ret:
            st.error("Error reading from webcam.")
            break

        # Initialize the video writer when the recording starts
        if video_writer is None:
            frame_height, frame_width = frame.shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(
                temp_file.name, fourcc, 20.0, (frame_width, frame_height)
            )

        # Display the live video feed
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame_bgr, channels="RGB")

        # Write the frame to the video file
        video_writer.write(frame)

    # Cleanup
    if video_writer:
        video_writer.release()
    cap.release()

    if not st.session_state.recording:
        st.success("Video recording stopped.")
        return temp_file.name

    return None


# Streamlit interface
st.title("Video Processing Application")

# Step 1: Record a video
st.header("Step 1: Record a Video")
recorded_video_path = record_video()

# Step 2: Process the video
if recorded_video_path:
    st.header("Step 2: Process the Video")
    process_button = st.button("Process Recorded Video")

    if process_button:
        # Temporary file to store the processed video
        processed_video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

        process_video(recorded_video_path, processed_video_path)

        st.video(processed_video_path)

        st.success("Video processed successfully!")
