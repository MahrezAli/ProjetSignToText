import os
import cv2

DATA_DIR = "./dataset"

# Création du répertoire de données s'il n'existe pas
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

nb_lettres = 24
class_size = 750
lettres = 'ABCDEFGHIKLMNOPQRSTUVWXY'

# Ouverture de la caméra
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erreur : La caméra n'a pas pu être ouverte.")
    exit()

# Boucle pour chaque lettre
for i in range(nb_lettres):
    letter_path = os.path.join(DATA_DIR, lettres[i])
    if not os.path.exists(letter_path):
        os.makedirs(letter_path)

    print(f'En cours de création de données pour la lettre : {lettres[i]}')

    # Affichage du message jusqu'à ce que l'utilisateur appuie sur 's'
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Échec de la capture d'une image")
            continue

        cv2.putText(frame, "Appuyer sur la lettre 's' pour commencer la collection", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (130, 200, 0), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        
        if cv2.waitKey(25) == ord('s'):
            break

    # Capture des images pour la lettre en cours
    compteur = 600
    while compteur < class_size:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(DATA_DIR, lettres[i], '{}.jpg'.format(compteur)), frame)

        compteur += 1

# Libération de la caméra et fermeture des fenêtres
cap.release()
cv2.destroyAllWindows()
