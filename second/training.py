import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')

lemmatizer = WordNetLemmatizer()

# Load intents from JSON file
with open('intents.json') as file:
    intents = json.load(file)

words = []
classes = []
documents = []
ignoreLetters = ['?', '!', '.', ',', 'a', 'an', 'and', 'are', 'be', 'do', 'have', 'i', 'in', 'is', 'me', 'of', 'that', 'the', 'to', 'you']

# Loop through intents to extract patterns and tags
for intent in intents['intents']:
    tag = intent['tag']
    if tag not in classes:
        classes.append(tag)

    for pattern in intent['patterns']:
        # Tokenize words from pattern
        try:
            wordList = nltk.word_tokenize(pattern)
        except Exception as e:
            print(f"Error tokenizing pattern '{pattern}': {e}")
            continue

        # Lemmatize and lowercase words, and add to words list
        words.extend([lemmatizer.lemmatize(word.lower()) for word in wordList if word not in ignoreLetters])

        # Add (words, tag) tuple to documents list
        documents.append((wordList, tag))

# Remove duplicates and sort words list
words = sorted(set(words))

# Save words and classes to pickle files
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Initialize training data and output array
training = []
outputEmpty = [0] * len(classes)

# Loop through documents to create bag of words and output rows
for document in documents:
    bag = []
    wordPatterns = document[0]
    wordPatterns = [lemmatizer.lemmatize(word.lower()) for word in wordPatterns]

    # Create bag of words
    for word in words:
        bag.append(1) if word in wordPatterns else bag.append(0)

    # Create output row
    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1

    # Append bag of words and output row to training data
    training.append(bag + outputRow)

random.shuffle(training)
training = np.array(training)

trainX = training[:, :len(words)]
trainY = training[:, len(words):]

model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, input_shape=(len(trainX[0]),), activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(len(trainY[0]), activation='softmax') ])


sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train model
model.fit(trainX, trainY, epochs=200, batch_size=5, verbose=1)

# Save model
model.save('chatbot_model.h5')
print('Done')
