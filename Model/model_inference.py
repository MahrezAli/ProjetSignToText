import cv2
import mediapipe as mp
import pickle
import numpy as np

# Configuration de l'instance MediaPipe pour le suivi des mains
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Chargement du modèle entraîné et de l'encodeur de labels
with open("./model.p", 'rb') as f:
    model = pickle.load(f)['model']

with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Ouverture de la caméra
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Conversion de l'image en RGB pour MediaPipe
    video_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    video_landmarks = hands.process(video_rgb)

    data_tmp = []

    xx = []
    yy = []

    Height, Width, _ = frame.shape

    # Si des mains sont détectées
    if video_landmarks.multi_hand_landmarks:
        for hand_landmarks in video_landmarks.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, 
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

            # Collecte des points de repère pour chaque articulation
            for landmark in hand_landmarks.landmark:
                data_tmp.extend([landmark.x, landmark.y, landmark.z])
                xx.append(landmark.x)
                yy.append(landmark.y)

        # Prédiction uniquement si le nombre de points de repère est correct
        if len(data_tmp) == 63:  # Vérification de la longueur attendue par le modèle
            prediction = model.predict([data_tmp])
            predicted_label = label_encoder.inverse_transform(prediction)
            print(predicted_label)
        else:
            print("Nombre de caractéristiques inattendu reçu:", len(data_tmp))

        x1 = int(min(xx) * Width)
        y1 = int(min(yy) * Height)

        x2 = int(max(xx) * Width)
        y2 = int(max(yy) * Height)

        # Dessiner un rectangle autour de la main détectée et afficher le label prédit
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,0), 5)
        cv2.putText(frame, predicted_label[0], (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (130, 200, 0), 3, cv2.LINE_AA)

    # Affichage de l'image
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Appuyer sur 'q' pour quitter
        break

# Libération de la caméra et fermeture des fenêtres
cap.release()
cv2.destroyAllWindows()
