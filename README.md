Here's a GitHub README for your Streamlit application, **FaceSearcher.ai**. This README includes sections on project overview, installation, usage, and contributing.

---

# FaceMatch.ai

FaceSearcher.ai is a real-time face recognition application built with Streamlit, OpenCV, and Firebase. The application identifies actors from live webcam feed, retrieves their information from a Firebase database, and displays it in a user-friendly interface.

## Features

- **Real-Time Face Recognition:** Uses webcam to capture live video and recognize faces.
- **Actor Information:** Fetches and displays information about recognized actors from Firebase.
- **Face Encoding:** Encodes face data and saves it for future recognition.
- **Interactive UI:** Shows recognized faces and relevant actor information in a clean Streamlit interface.

## Installation

To run FaceSearcher.ai, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/facematch-ai.git
   cd facesearcher-ai
   ```

2. **Create a Virtual Environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Firebase:**

   - Create a Firebase project and download the `serviceAccountKey.json` file.
   - Replace `"actor-and-actress-firebase-adminsdk-8skz5-a9185b831c.json"` in the code with your downloaded Firebase Admin SDK JSON file.

5. **Prepare the Face Data:**

   - Place your face images in the `Data` folder.
   - Run the encoding script to generate the face encodings and save them:

     ```bash
     python encode_faces.py
     ```

## Usage

1. **Run the Streamlit Application:**

   ```bash
   streamlit run app.py
   ```

2. **Interact with the Application:**

   - The webcam feed will be displayed.
   - Recognized faces will be highlighted with bounding boxes.
   - Actor names and details will appear in the sidebar.
   - Confidence levels and additional actor information will be shown as they are recognized.

## Code Overview

- **`main.py`**: Main Streamlit application file for real-time face recognition and UI display.
- **`face_encoder.py`**: Script to encode face images and upload them to Firebase.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Commit your changes and push to your forked repository.
4. Submit a pull request.

Please ensure your code follows the project's style guide and includes relevant tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io) - Framework for building the web app.
- [OpenCV](https://opencv.org) - Library for computer vision tasks.
- [face_recognition](https://github.com/ageitgey/face_recognition) - Library for face recognition.
- [Firebase](https://firebase.google.com) - Backend for storing face encodings and actor information.

---

Feel free to modify any sections according to your project's specific needs or details.
![Ekran görüntüsü 2024-08-24 134250](https://github.com/user-attachments/assets/77e97eb6-64fd-469f-b8b8-666c16245696)
