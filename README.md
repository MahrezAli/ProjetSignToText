Le Projet contient 3 Dossiers :

-    Model est le dossier qui permet la création du modèle ML à partir du dataset collecté. Il y a 4 fichiers a executer dans l'ordre: - createDataset.py qui collecte les images puis les stocke dans un dossier dataset par lettre - pre_processing.py qui recupere les landmarks de mains contenu dans les images collectées pour créer un dataset (data : landmarks) et (label : lettre) - model_training.py qui entraine le modèle à partir du dataset crée (Modèle utilisé Random Forest) - model_inference.py qui permet de tester le modèle en affichant les valeurs prédite dans la vidéo

-    modelDocker qui est le dossier pour créer une image docker de notre modèle qu'on pourra requếter. Il y a 5 fichiers :
        app.py qui est l'API flask pour requeter le modèle à partir d'une adresse http (Localhost dans notre cas)
        Dockerfile qui créer une image de notre projet sur docker
        label_encoder.pkl qui correspond au labelEncoder utilisé lors de l'entrainement de notre modèle RandomForest pour déchiffrer les valeurs prédite
        model.p qui correspond à notre modèle RandomForest
        Requirements.txt qui contient les modules ou librairies à installer dans l'nevironnement docker

    Pour créer l'image, il faut se mettre dans le répertoir modelDocker puis executer: ```docker build -t hand_sign_recognition:latest .```

    Pour executer l'image, il faut executer la commande: ```docker run -p 5000:5000 hand_sign_recognition:latest```

-    Interface qui pour tester le modèle sur un site web correspond à notre interface web: Il y a 3 fichiers:
        SignToText.html qui correspond à la page web
        code.js qui est le code javascript pour requeter le modèle mais aussi pour afficher les résulats prédit sur la page HTML
        interface.css : code css pour présenter la page

