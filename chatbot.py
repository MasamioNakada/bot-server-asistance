
import random
import json
import pickle
import numpy as np
import en_core_web_sm
nlp = en_core_web_sm.load()


from nltk.stem import  WordNetLemmatizer

from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

model = load_model('chatbot_model.h5')

def clean_up_sentence(sentence):
    words_list = []
    sentence_words = nlp(sentence)
    sentence_words = [tok.lemma_.lower() for tok in sentence_words]
    for tok in sentence_words:
        words_list.append(str(tok))
    return words_list

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    print(return_list)
    return return_list

def get_response(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            print("achou tag %s"%(tag))
            result = i
            break
    return result

def wikibot_test(msg):
    ints = predict_class(msg, model)
    return ints

def wikibot(msg):
    ints = predict_class(msg, model)
    print(ints)
    res = get_response(ints, intents)
    return res

if __name__ == "__main__":
    print(wikibot('Hola'))