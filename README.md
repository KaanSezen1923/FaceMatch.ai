
# FaceMatch.ai

FaceMatch.ai is a Streamlit-based web application designed to recognize actors' faces in video frames and display their information retrieved from Firebase and TMDB (The Movie Database). The project involves encoding faces from images, saving these encodings and actor details in a Firebase Realtime Database, and then using a webcam or video input to recognize faces in real-time.

## Features

- **Real-time Face Recognition**: Detect and recognize faces from live video streams or video files.
- **Firebase Integration**: Store and retrieve actor face encodings and information from Firebase Realtime Database.
- **TMDB API Integration**: Fetch actor details such as biography, birthday, and place of birth from The Movie Database.
- **Streamlit Interface**: User-friendly interface to display the video, recognized faces, and actor information.

## Project Structure

```
.
├── Data                    # Folder containing images of actors to encode
├── EncodeFile.p            # Pickle file containing encoded face data
├── actor-and-actress-firebase-adminsdk.json  # Firebase credentials file
├── main.py                  # Main Streamlit application file
├── face_encoder.py         # Script to encode faces and save to Firebase
├── requirements.txt        # Python dependencies
└── README.md               # Project README file
```

## Deployment

### 1. Prepare Your Environment

- **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/FaceMatch.ai.git
   cd FaceMatch.ai
   ```

- **Create a Virtual Environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

- **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### 2. Set Up Firebase

- Place your Firebase Admin SDK JSON credentials file (`actor-and-actress-firebase-adminsdk.json`) in the root directory.
- Ensure the Firebase Realtime Database URL in the script matches your Firebase project settings.

### 3. Configure TMDB API

- Obtain a TMDB API key from [The Movie Database](https://www.themoviedb.org/).
- Replace `tmdb_api_key` in the `face_encoder.py` script with your TMDB API key.

### 4. Encode Faces and Store in Firebase

Run the `face_encoder.py` script to encode faces from images in the `Data` folder and store the encodings in Firebase Realtime Database:

```bash
python face_encoder.py
```

### 5. Run the Streamlit Application

Start the Streamlit application:

```bash
streamlit run main.py
```

This will open the application in your default web browser. The application will capture video from your webcam (or the specified video file) and display recognized faces along with their information.

## Configuration

- **Video Input:** Modify the `cv2.VideoCapture()` function in `main.py` to switch between a webcam and a video file.
- **Recognition Threshold:** Adjust the face recognition threshold in the main loop of `main.py` to fine-tune recognition accuracy.

## Dependencies

- Python 3.7+
- OpenCV
- face_recognition
- Firebase Admin SDK
- Streamlit
- cvzone
- requests
- numpy
- pickle

## Future Improvements

- Support for recognizing multiple faces simultaneously.
- Enhanced user interface with more detailed actor information.
- Caching TMDB API requests to reduce API call frequency.
- Expand the application to handle larger actor databases.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements, features, or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Make sure to adjust the repository URL and other specific details as needed.
