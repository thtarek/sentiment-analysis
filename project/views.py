from django.shortcuts import render
from django.views import View 
from django.http import HttpResponse
import pickle
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

import string
tfidf = pickle.load(open("models/vectorize.pkl","rb"))
mnb = pickle.load(open("models/mnb.pkl","rb"))

# Create your views here.


ps = PorterStemmer()
def remove_tags(raw_text):
        cleaned_text = re.sub(re.compile('<.*?>'), '', raw_text)
        return cleaned_text

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()
    
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
               
    return " ".join(y)

class EnterComment(View):
    def get(self,request):
        return render(request,"main/index.html")
    def post(self,request):
        raw_text = request.POST.get('comment') 
        remove_tag = remove_tags(raw_text)
        transformed_review = transform_text(remove_tag)
        vector_input = tfidf.transform([transformed_review])
        result = mnb.predict(vector_input)[0]
        if result == 1:
            sentiment = 'Positive'
        else:
            sentiment = 'Negative'

        context = {
            'sentiment' : sentiment
        }
        
        return render(request, 'main/index.html', context)



