import streamlit as st
import pickle
import cv2
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials, db
import cvzone

# Page configuration
st.set_page_config(page_title="FaceSearcher.ai", layout="centered")

# Firebase initialization
cred = credentials.Certificate("actor-and-actress-firebase-adminsdk-8skz5-a9185b831c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://actor-and-actress-default-rtdb.firebaseio.com/'
})

@st.cache_data
def load_encoded_faces(file_path):
    """Load and return encoded face data from a pickle file."""
    try:
        with open(file_path, "rb") as file:
            encode_list_known_with_names = pickle.load(file)
            return encode_list_known_with_names
    except FileNotFoundError:
        st.error("Encoding file not found. Please check the file path.")
        st.stop()

def fetch_actor_info(name):
    """Retrieve actor information from Firebase based on the name."""
    ref = db.reference('face_encodings')
    actors = ref.get()
    return next((actor['actor_info'] for actor in actors.values() if actor['name'] == name), None)

def display_actor_info(actor_info):
    """Display the actor's biography, birthday, and place of birth in a table format."""
    if actor_info:
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)
        
        col1.write("**Biography:**")
        col2.write(actor_info.get('biography', 'N/A'))
        
        col3.write("**Birthday:**")
        col4.write(actor_info.get('birthday', 'N/A'))
        
        col5.write("**Place of Birth:**")
        col6.write(actor_info.get('place_of_birth', 'N/A'))
    else:
        st.warning("No additional information found for this actor in Firebase.")

# Application title
st.title("FaceSearcher.ai")

# Load face encodings
st.info("Loading encoded face data...")
encode_list_known, names = load_encoded_faces("EncodeFile.p")
st.success("Encoding file loaded successfully.")

# Initialize webcam video capture
cap = cv2.VideoCapture("Yüzüklerin Efendisi Yüzük Kardeşliği _ Kardeşlik Kuruluyor _ HD İzle.mp4")
stframe = st.empty()

actor_info_container = st.empty()

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

    if face_encodings:
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

                # Fetch and display actor information if a new face is recognized
                if actor_name != last_actor_name:
                    last_actor_info = fetch_actor_info(actor_name)
                    last_actor_name = actor_name

                    # Display actor information on the sidebar
                    st.sidebar.subheader(f"Match Found: {actor_name}")
                    st.sidebar.write(f"Confidence: {round((1 - face_distances[match_index]) * 100, 2)}%")
                    actor_info_container.empty()
                    with actor_info_container.container():
                        display_actor_info(last_actor_info)
            else:
                st.sidebar.warning("No match found.")

    # Display the annotated frame
    stframe.image(frame, channels="BGR")

# Release the video capture object
cap.release()

