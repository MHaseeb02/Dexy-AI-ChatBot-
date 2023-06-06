import random
import pickle
import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf

lemmatizer = WordNetLemmatizer() #setting up a lemmatizer
intents = json.loads(open("intents.json", encoding="utf8").read())  #loading the dataset

#setting up some paramenters for future use
words = []
classes = []
documents = []
ignore_words = ["!","@","#","$","%","^","&","*","(",")",'+',"=","[","]","{","}",".",'<',">",",","?","/","|","-","_","~","`","'",'"',":",";"]

#getting the entire dataset in form of patterns and tags
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list ,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

#lemmitizing all the words in the words list and sorting them out
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_words]
words = sorted(set(words))
classes = sorted(set(classes))

#saving the data into a pickle file for future use
pickle.dump(words, open("words.pkl","wb"))
pickle.dump(classes, open("classes.pkl","wb"))

#creating a traning list for training
training = []
output_empty = [0] * len(classes)

#creating a bag of words along with its tag or class
for document in documents:
    bag=[]
    word_patterns = document[0]
    word_patterns=[lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)   
    
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append(bag + output_row)

#shuffleing the training data
random.shuffle(training)
training = np.array(training)

#creating the training data parameters
train_x = training[:,:len(words)] #for worrds
train_y = training[:,len(words):] #for classes

#creating the training model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(320, input_shape = (len(train_x[0]),), activation= 'relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(200, activation= 'relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(len(train_y[0]), activation= 'softmax')
])

#training the data
sgd = tf.keras.optimizers.SGD(learning_rate = 0.01, momentum=0.9, nesterov=True)
model.compile(loss = 'categorical_crossentropy',optimizer=sgd, metrics=['accuracy'])
MM = model.fit(train_x, train_y, epochs = 500, batch_size =22, verbose = 1)
model.save("model1.h5",MM)
print("Done")