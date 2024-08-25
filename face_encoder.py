import os
import face_recognition
import cv2
import pickle
import firebase_admin
from firebase_admin import credentials, db
import requests

# Firebase'e bağlanma
cred = credentials.Certificate("actor-and-actress-firebase-adminsdk-8skz5-a9185b831c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://actor-and-actress-default-rtdb.firebaseio.com/'
})

folder_path = "Data"

# TMDB API bilgileri
tmdb_api_key = "YOUR API KEY HERE"
tmdb_base_url = "https://api.themoviedb.org/3"

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

def get_actor_info(name):
    search_url = f"{tmdb_base_url}/search/person"
    params = {
        "api_key": tmdb_api_key,
        "query": name
    }
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            actor_id = results[0]['id']
            details_url = f"{tmdb_base_url}/person/{actor_id}"
            details_params = {"api_key": tmdb_api_key}
            details_response = requests.get(details_url, params=details_params)
            if details_response.status_code == 200:
                return details_response.json()
    return None

for i in range(len(encode_list_known)):
    face_data = {
        "name": names[i],
        "encoding": encode_list_known[i].tolist()  # Numpy array'i JSON uyumlu yapmak için listeye çeviriyoruz
    }
    
    actor_info = get_actor_info(names[i])
    if actor_info:
        face_data["actor_info"] = {
            "biography": actor_info.get("biography", ""),
            "birthday": actor_info.get("birthday", ""),
            "place_of_birth": actor_info.get("place_of_birth", ""),
            "known_for": [movie["title"] for movie in actor_info.get("known_for", [])]
        }
    
    ref.child(names[i]).set(face_data)
    print(f"Saved {names[i]} to Firebase Realtime Database")

print("Encoding completed and saved to Firebase Realtime Database and pickle file successfully.")


