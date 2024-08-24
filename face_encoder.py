import os
import face_recognition
import cv2
import pickle
import firebase_admin
from firebase_admin import credentials, db

# Firebase'e bağlanma
cred = credentials.Certificate("actor-and-actress-firebase-adminsdk-8skz5-a9185b831c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://actor-and-actress-default-rtdb.firebaseio.com/'
})

folder_path = "Data"

# Klasördeki dosyaları listeleme
try:
    pathlist = os.listdir(folder_path)
    if not pathlist:
        raise ValueError("No files found in the specified directory.")
    print(f"Found {len(pathlist)} files in {folder_path}.")
except Exception as e:
    print(f"Error: {e}")
    exit()

images = []
names = []

# Resimleri yükleme ve isimlerini ayıklama
for path in pathlist:
    img_path = os.path.join(folder_path, path)
    img = cv2.imread(img_path)
    if img is None:
        print(f"Warning: Couldn't read image {img_path}. Skipping...")
        continue
    
    images.append(img)
    names.append(os.path.splitext(path)[0])
    
print(f"Images processed: {len(images)}")
print(f"Names extracted: {names}")

def find_encodings(images_list):
    encode_list = []
    for img in images_list:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        print(f"Processing image with shape: {img_rgb.shape}")
        
        face_locations = face_recognition.face_locations(img_rgb)
        if not face_locations:
            print("Warning: No face found in the image. Skipping...")
            continue
        
        face_encoding = face_recognition.face_encodings(img_rgb)[0]
        encode_list.append(face_encoding)
    
    return encode_list

print("Starting face encoding...")
encode_list_known = find_encodings(images)

if not encode_list_known:
    print("No faces were encoded. Exiting...")
    exit()

# Encode edilmiş veriyi pickle dosyasına kaydetme
encode_list_known_with_names = [encode_list_known, names]

output_file = "EncodeFile.p"
try:
    with open(output_file, "wb") as file:
        pickle.dump(encode_list_known_with_names, file)
    print(f"Encoded data saved to {output_file}")
except Exception as e:
    print(f"Error saving file: {e}")

# Realtime Database'e kaydetme
ref = db.reference("face_encodings")

for i in range(len(encode_list_known)):
    face_data = {
        "name": names[i],
        "encoding": encode_list_known[i].tolist()  # Numpy array'i JSON uyumlu yapmak için listeye çeviriyoruz
    }
    ref.child(names[i]).set(face_data)
    print(f"Saved {names[i]} to Firebase Realtime Database")

print("Encoding completed and saved to Firebase Realtime Database and pickle file successfully.")


