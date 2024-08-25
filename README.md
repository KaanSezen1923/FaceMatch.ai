Here's a `README.md` file for your project:

---

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

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/FaceMatch.ai.git
   cd FaceSearcher.ai
   ```

2. **Install Dependencies:**

   You can install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Firebase:**

   - Place your Firebase Admin SDK JSON credentials file (`actor-and-actress-firebase-adminsdk.json`) in the root directory.
   - Make sure to update the Firebase Realtime Database URL in the script if necessary.

4. **TMDB API Key:**

   - Obtain a TMDB API key from [The Movie Database](https://www.themoviedb.org/).
   - Replace `tmdb_api_key` in the `face_encoder.py` script with your TMDB API key.

## Usage

### 1. Encoding Faces and Storing in Firebase

   Run the `face_encoder.py` script to encode faces from the images in the `Data` folder and store the encodings in Firebase Realtime Database:

   ```bash
   python face_encoder.py
   ```

   This script will process all images in the `Data` folder, encode the faces, and save the encodings along with the actor's information in Firebase.

### 2. Running the Streamlit Application

   After encoding the faces, you can run the main application using Streamlit:

   ```bash
   streamlit run main.py
   ```

   This will open the application in your default web browser. The application will start capturing video from your webcam (or the specified video file) and display recognized faces along with their information on the sidebar.

## Configuration

- **Video Input:** You can change the video source in the `main.py` file by modifying the `cv2.VideoCapture()` function. For example, you can switch between a webcam and a video file.
- **Threshold for Face Recognition:** The face recognition threshold is set to `0.65` by default. You can adjust this threshold in the main loop to make the recognition more or less strict.

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

- Add support for recognizing multiple faces simultaneously.
- Improve the user interface with more detailed actor information.
- Implement caching for TMDB API requests to reduce the number of API calls.
- Expand the application to handle larger databases of actors.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements, features, or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This `README.md` should provide a clear overview of your project, guiding users through installation, usage, and configuration. Make sure to adjust the repository URL and other specific details as needed.
