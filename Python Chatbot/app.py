from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import numpy as np
import random
import spacy
from sklearn.neural_network import MLPClassifier
from docx import Document
import PyPDF2

# Initialize Flask and spaCy
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
nlp = spacy.load("en_core_web_sm")

# Define intents
intents = [
    {
        "tag": "greeting",
        "patterns": ["Hi", "Hello", "Hey there", "What's up", "Greetings"],
        "responses": ["Hello!", "Hi there!", "Hey!", "Greetings!", "How can I assist you?"]
    },
    {
        "tag": "goodbye",
        "patterns": ["Bye", "See you later", "Goodbye", "I'm leaving"],
        "responses": ["Goodbye!", "See you later!", "Farewell!", "Have a great day!"]
    },
    {
        "tag": "thanks",
        "patterns": ["Thanks", "Thank you", "I appreciate it", "Thanks a lot"],
        "responses": ["You're welcome!", "No problem!", "Anytime!", "Glad I could help!"]
    },
    {
        "tag": "weather",
        "patterns": ["What's the weather like?", "Tell me about the weather", "Is it sunny?"],
        "responses": ["I'm not a weather app, but I can try to help. It's always a good idea to check your weather app for accurate info!"]
    },
    {
        "tag": "name",
        "patterns": ["What is your name?", "Who are you?", "What should I call you?"],
        "responses": ["I am your chatbot assistant!", "You can call me Chatbot!", "I'm here to assist you!"]
    },
    {
        "tag": "age",
        "patterns": ["How old are you?", "What is your age?", "When were you created?"],
        "responses": ["I am ageless!", "I was created just for you!", "Old enough to assist you!"]
    },
    {
        "tag": "joke",
        "patterns": ["Tell me a joke", "Make me laugh", "I need a joke"],
        "responses": ["Why did the scarecrow win an award? Because he was outstanding in his field!", "Why don't skeletons fight each other? They don't have the guts."]
    }
]

# Prepare training data
all_words = []
tags = []
documents = []

for intent in intents:
    for pattern in intent["patterns"]:
        doc = nlp(pattern.lower())
        tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop]
        all_words.extend(tokens)
        documents.append((tokens, intent["tag"]))
    if intent["tag"] not in tags:
        tags.append(intent["tag"])

all_words = sorted(set(all_words))
tags = sorted(tags)

training = []
output_empty = [0] * len(tags)

for document in documents:
    bag = [1 if word in document[0] else 0 for word in all_words]
    output_row = list(output_empty)
    output_row[tags.index(document[1])] = 1
    training.append([bag, output_row])

training = np.array(training, dtype=object)
train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = MLPClassifier(hidden_layer_sizes=(8, 8), max_iter=500)
model.fit(train_x, train_y)

# Function to parse uploaded files
def parse_file(filepath):
    if filepath.endswith('.txt'):
        with open(filepath, 'r') as file:
            text = file.read()
    elif filepath.endswith('.docx'):
        doc = Document(filepath)
        text = '\n'.join([p.text for p in doc.paragraphs])
    elif filepath.endswith('.pdf'):
        text = ""
        with open(filepath, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text()
    else:
        text = ""
    return text

# Route to upload a file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    text = parse_file(filepath)
    return jsonify({"success": f"File {filename} uploaded and parsed!", "content": text[:500]})

# Route for chatbot interaction
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    bow = bag_of_words(user_input, all_words)
    result = model.predict([bow])[0]
    tag = tags[np.argmax(result)]

    for intent in intents:
        if intent["tag"] == tag:
            return jsonify({"response": random.choice(intent["responses"])})
    return jsonify({"response": "I'm not sure how to help with that!"})

def bag_of_words(sentence, words):
    doc = nlp(sentence.lower())
    sentence_words = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop]
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

if __name__ == "__main__":
    app.run(debug=True)
