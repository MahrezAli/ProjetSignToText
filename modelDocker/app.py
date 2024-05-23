from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np
import mediapipe as mp
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialisation des modules de MediaPipe pour la détection des mains
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Configuration de MediaPipe pour détecter les mains dans des images statiques
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Chargement du modèle pré-entraîné pour la prédiction
with open("./model.p", 'rb') as f:
    model = pickle.load(f)['model']

# Chargement de l'encodeur de labels
with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Fonction pour décoder une image en base64 en une image utilisable
def decode_image(base64_string):
    img_data = base64.b64decode(base64_string.split(',')[1])
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

# Définition de la route pour la prédiction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_base64 = data['image']
    image = decode_image(image_base64)
    
    # Conversion de l'image en RGB pour MediaPipe
    video_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    video_landmarks = hands.process(video_rgb)

    data_tmp = []
    landmarks = []

    # Extraction des points de repère de la main si détectée
    if video_landmarks.multi_hand_landmarks:
        for hand_landmarks in video_landmarks.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                data_tmp.extend([landmark.x, landmark.y, landmark.z])
                landmarks.append({"x": landmark.x, "y": landmark.y, "z": landmark.z})

        # Prédiction avec le modèle si 21 points de repère sont détectés (21*3=63)
        if len(data_tmp) == 63:
            prediction = model.predict([data_tmp])
            predicted_label = label_encoder.inverse_transform(prediction)[0]
        else:
            predicted_label = "Inconnu"
    else:
        predicted_label = "Aucune main détectée"

    return jsonify({"label": predicted_label, "landmarks": landmarks})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
