import mediapipe as mp
import cv2
import os
import matplotlib.pyplot as plt
import pickle

DATA_DIR = "./dataset"

# Initialisation des modules MediaPipe pour le suivi des mains
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

data = []
labels = []

# Utilisation de MediaPipe pour traiter les images dans le répertoire de données
with mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3) as hands:
    for letter in os.listdir(DATA_DIR):
        if letter != '.DS_Store':  # Ignorer les fichiers système cachés
            for img_name in os.listdir(os.path.join(DATA_DIR, letter)):
                if '.DS_Store' not in img_name:  # Ignorer les fichiers système cachés
                    data_tmp = []
                    img_path = os.path.join(DATA_DIR, letter, img_name)
                    img = cv2.imread(img_path)
                    if img is not None:
                        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                        img_landmarks = hands.process(img_rgb)
                        if img_landmarks.multi_hand_landmarks:
                            for hand_landmarks in img_landmarks.multi_hand_landmarks:
                                for i in range(len(hand_landmarks.landmark)):
                                    x = hand_landmarks.landmark[i].x
                                    y = hand_landmarks.landmark[i].y
                                    z = hand_landmarks.landmark[i].z
                                    data_tmp.append(x)
                                    data_tmp.append(y)
                                    data_tmp.append(z)

                            data.append(data_tmp)
                            labels.append(letter)

# Sauvegarde des données et des labels dans un fichier pickle
f = open('./data.pickle', 'wb')
pickle.dump({'data': data, 'labels': labels}, f)
f.close()
