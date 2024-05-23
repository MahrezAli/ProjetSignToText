import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Charger le dictionnaire de données
data_dict = pickle.load(open("./data.pickle", 'rb'))
data = data_dict['data'] 
labels = data_dict['labels'] 

# Initialiser le LabelEncoder
label_encoder = LabelEncoder()

# Encoder les labels
encoded_labels = label_encoder.fit_transform(labels)

# Filtrer les indices où les vecteurs de caractéristiques ont la longueur correcte
valid_indices = [i for i, item in enumerate(data) if len(item) == 63]

# Filtrer X et y en utilisant ces indices
X_filtered = [data[i] for i in valid_indices]
y_filtered = [encoded_labels[i] for i in valid_indices]

# Convertir en tableaux numpy
X = np.array(X_filtered)
y = np.array(y_filtered)

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, stratify=y)

# Initialiser et entraîner le RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Prédire sur l'ensemble de test
predictions = model.predict(X_test)

# Calculer et afficher la précision
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)


f = open('./model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()


with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)



