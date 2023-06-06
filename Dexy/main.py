import random
import pickle
import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf

lemmatizer = WordNetLemmatizer()
intents = json.loads(open("intents.json",encoding="utf8").read())
words=pickle.load(open('words.pkl','rb'))
classes=pickle.load(open('classes.pkl','rb'))
model=tf.keras.saving.load_model('model1.h5')

#first we need to clean up the sentence the user wil enter
def clean_up_sentence(sentence):
    sentence_words=nltk.word_tokenize(sentence.lower())
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

#now lets create a bag of words for that sentence
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i,word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

#now lets predict the class in the the question lies
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    error_threshold = 0.25   # 25%
    result = [[i,r] for i,r in enumerate(res) if r > error_threshold]
    result.sort(key= lambda x:x[1], reverse= True)
    return_list = []
    for r in result:
        return_list.append({'intents' : classes[r[0]],'probability' : str(r[1])})
    return return_list

#now lets get the responce from the user
def get_responces(intents_list,intent_json):
    try : 
        tag = intents_list[0]['intents']
        list_of_intents = intent_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result
    except : 
        return "Sorry I didn't really undershoot what you ment"

#to run the application
# while True:
#     message = input("You: ")
#     intent_list = predict_class(message)
#     result = get_responces(intent_list,intents)
#     print("Dexy: "+result)