var predictedLetter = "";
var lastTimePredicted = Date.now();
var accumulateTime = 2500; // 3 secondes pour la validation
var confirmedLetters = "";
var suggestedWords = [];
var confirmedSentence = "";  // Stocke la phrase complète
var confirmedWords = [];     // Stocke les mots confirmés individuellement

navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(stream) {
        var video = document.getElementById('video');
        video.srcObject = stream;
        video.play();
    })
    .catch(function(err) {
        console.log("An error occurred: " + err);
    });

function captureFrame() {
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var video = document.getElementById('video');

    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    var dataURL = canvas.toDataURL('image/jpeg');

    fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: dataURL })
    })
        .then(response => response.json())
        .then(data => {
            processPrediction(data.label);
        })
        .catch(error => console.error('Error:', error));
}

function processPrediction(label) {
    console.log(label);
    if (predictedLetter !== label) {
        predictedLetter = label;
        lastTimePredicted = Date.now();
    } else if (Date.now() - lastTimePredicted >= accumulateTime && label.length == 1) {
        confirmedLetters += label;
        predictedLetter = ""; // Réinitialiser après confirmation
        generateWordSuggestions();
    }
    displayResult(label);
}

function generateWordSuggestions() {
    var apiUrl = 'https://api.datamuse.com/words?sp=' + confirmedLetters + '*&max=3';

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            suggestedWords = data.map(wordObj => wordObj.word);
            displaySuggestions();
        })
        .catch(error => console.error('Error fetching word suggestions:', error));
}

function displayResult(label) {
    var resultDiv = document.getElementById('result');
    var labelStyle = "font-size: 0.8em; font-style: italic; color: white;"; // Style pour les labels
    var contentStyle = "font-size: 0.9em; font-family: 'Arial', sans-serif;"; // Style pour le contenu
    resultDiv.innerHTML = "<span style='" + labelStyle + "'>Predicted Label:</span> <span style='" + contentStyle + "'>" + label + "</span><br/><span style='" + labelStyle + "'>Current Word:</span> <span style='" + contentStyle + "'>" + confirmedLetters + "</span>";
}

function displaySuggestions() {
    var suggestionsContainer = document.getElementById('suggestions');
    suggestionsContainer.innerHTML = ""; // Nettoie les suggestions précédentes

    suggestedWords.forEach(function(word) {
        var wordButton = document.createElement('button');
        wordButton.textContent = word;
        wordButton.onclick = function() { addWordToSentence(word); };
        suggestionsContainer.appendChild(wordButton);
    });
}

function addWordToSentence(selectedWord) {
    confirmedWords.push(selectedWord);
    confirmedSentence += selectedWord + " ";  // Ajoute le mot à la phrase avec un espace
    confirmedLetters = "";  // Réinitialise pour la nouvelle prédiction de mot
    predictedLetter = "";   // Réinitialise la lettre en cours de prédiction
    suggestedWords = [];    // Nettoie les suggestions précédentes

    updateUI();  
}

function updateUI() {
    var sentenceDiv = document.getElementById('sentence');
    sentenceDiv.innerHTML = "Sentence : " + confirmedSentence;
    displaySuggestions();
}

document.getElementById('ok-button').addEventListener('click', addCurrentWordToSentence);

function addCurrentWordToSentence() {
    if (confirmedLetters.length > 0) {
        confirmedSentence += confirmedLetters + " ";
        confirmedLetters = "";  
        predictedLetter= "";
        suggestedWords = [];
        updateUI();  
    }
}


function resetSentence() {
    confirmedSentence = "";
    confirmedLetters = "";
    updateUI();
}

document.getElementById('validate-button').addEventListener('click', resetSentence);

setInterval(captureFrame, 100);

