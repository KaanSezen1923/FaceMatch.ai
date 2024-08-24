import streamlit as st
import pickle
import cv2
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials, db
import cvzone

# Set up the Streamlit page configuration
st.set_page_config(page_title="FaceMatch.ai", layout="centered")

# Initialize Firebase connection
cred = credentials.Certificate("actor-and-actress-firebase-adminsdk-8skz5-a9185b831c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://actor-and-actress-default-rtdb.firebaseio.com/'
})

def get_actor_info(name):
    """Fetch actor information from Firebase by name."""
    ref = db.reference('face_encodings')
    actors = ref.get()
    if actors:
        for actor in actors.values():
            if actor['name'] == name:
                return actor
    return None

# Display the title of the application
st.title("FaceMatch.ai")

# Load known face encodings
st.info("Loading encoded face data...")
try:
    with open("EncodeFile.p", "rb") as file:
        encode_list_known_with_names = pickle.load(file)
        encode_list_known, names = encode_list_known_with_names
    st.success("Encoding file loaded successfully.")
except FileNotFoundError:
    st.error("Encoding file not found. Please check the file path.")
    st.stop()

# Initialize webcam video capture
cap = cv2.VideoCapture(0)
stframe = st.empty()

# Variables to keep track of the last recognized face
last_actor_name = None
last_actor_info = None

# Main loop to process video frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        st.warning("Failed to capture frame from video.")
        break
    
    # Convert the frame to RGB for face_recognition processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face locations and encodings in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        face_distances = face_recognition.face_distance(encode_list_known, face_encoding)
        match_index = np.argmin(face_distances)

        # Check if the closest match is within the acceptable threshold
        if face_distances[match_index] <= 0.65:
            actor_name = names[match_index]



            # Draw a rectangle around the face
            top, right, bottom, left = face_location
            bbox = (left, top, right - left, bottom - top)
            cvzone.cornerRect(frame, bbox)
            
            # Display the actor's name using cvzone
            cvzone.putTextRect(frame, actor_name, (left, top - 15))
            
            if actor_name != last_actor_name:
                last_actor_info = get_actor_info(actor_name)
                last_actor_name = actor_name

                # Display actor information on the sidebar
                st.sidebar.subheader(f"Match Found: {actor_name}")
                st.sidebar.write(f"Confidence: {round((1 - face_distances[match_index]) * 100, 2)}%")
                if last_actor_info:
                    for key, value in last_actor_info.items():
                        if key not in ["encoding", "name"]:
                            st.sidebar.write(f"**{key.capitalize()}:** {value}")
                else:
                    st.sidebar.warning("No additional information found for this actor in Firebase.")
        else:
            st.sidebar.warning("No match found.")

    # Display the annotated frame
    stframe.image(frame, channels="BGR")

# Release the video capture object
cap.release()

