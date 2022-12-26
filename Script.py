import re
import pandas as pd
from nltk.corpus import stopwords 
from nltk.tokenize import TweetTokenizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
factory = StemmerFactory()
stemmer = factory.create_stemmer()
stopwords_indonesia = stopwords.words('indonesian')


def lowercase(text):
    new_text = text.lower()
    return new_text


def remove_unnecessary_char(text):
    text = re.sub(r'\\n',' ', text)
    text = re.sub('rt','', text)
    text = re.sub('user','', text)
    text = re.sub('url','', text)
    text = re.sub(';','', text)
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text)
    text = re.sub('  +',' ', text)
    text = re.sub('\d+\.\s',' ', text)
    text = re.sub(r'x[a-z0-9][a-z0-9]','',text)
    return text


def remove_nonaplhanumeric(text):
    text = re.sub(r'[^0-9a-zA-Z\?!,.]+', ' ', text)
    text = re.sub('"','', text)
    text = re.sub('\s\s+' , ' ', text)
    text = re.sub('^\s','', text)
    return text


def remove_duplicateexclamation(text):
    text = re.sub(r'[!]{2,}', '!', text)
    text = re.sub(r'[\?]{2,}', '?', text)
    text = re.sub(r'(! ){2,}', '!', text)
    text = re.sub(r'(\? ){2,}', '?', text)
    text = re.sub(r',{2,}', ',', text)
    text = re.sub(r'\.{2,}', ',', text)
    return text


 
def normalize_alay(text):
    kamus_alay = pd.read_csv('source/new_kamusalay.csv', encoding='latin-1')
    alay_dict_map = dict(zip(kamus_alay['alay'], kamus_alay['arti']))
    for word in alay_dict_map:
        normalized_word = ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in text.split(' ')])
        return normalized_word



def process_word(text):
    text = lowercase(text)
    text = remove_unnecessary_char(text)
    text = remove_nonaplhanumeric(text)
    text = remove_duplicateexclamation(text)
    text = normalize_alay(text)
    text = remove_stopwords(text)
    return text

def remove_stopwords(text):
    # tokenize tweets
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tweet_tokens = tokenizer.tokenize(text)
 
    tweets_clean = []    
    for word in tweet_tokens:
        if (word not in stopwords_indonesia): # remove stopwords
            #tweets_clean.append(word)
            stem_word = stemmer.stem(word) # stemming word
            tweets_clean.append(stem_word)
    return " ".join(tweets_clean)



list = ['a']