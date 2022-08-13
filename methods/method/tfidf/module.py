import math

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from database import retrieve
from preprocessing import preprocessing
from preprocessing.stopword import stopwords


def bagOfWord(docs):
    unique = []
    for judul in docs:
        for keyword in judul:
            if keyword not in unique:
                unique.append(keyword)
    unique.sort()
    bow = []
    for judul in docs:
        temp = dict.fromkeys(unique, 0)
        for kata in judul:
            if len(kata) >= 2:
                temp[kata] = judul.count(kata)
        bow.append(temp)
    return bow

def termFrequency(bow):
    tf = []
    for judul in bow:
        temp = dict.fromkeys(judul.keys(), 0)
        for kata, total in judul.items():
            if total > 0 :
                temp[kata] = total / len([i for i in judul.keys() if judul[i] > 0])
        tf.append(temp)
    return tf

def inverseDocumentFrequency(docs):
    N = len(docs)
    idf = dict.fromkeys(docs[0].keys(), 0)
    for doc in docs:
        for word, tf in doc.items():
            if tf > 0:
                idf[word] += 1
    for word, value in idf.items():
        idf[word] = math.log((1+N) / float(1+value)) + 1
    return idf

def indexingTfidf():

    return

def calculateTfidf(tf, idf):
    tfidf = {}
    for kata, value in tf.items():
        tfidf[kata] = value * idf[kata]
    return tfidf

def similarity(query):

    return

if __name__ == "__main__":
    data = retrieve()
    # judul = [i['preprocessed']['result'] for i in data]
    judul = [i.split(" ") for i in ["deteksi penyakit tuberculosis","deteksi dini penyakit jantung"]]
    query = "deteksi penyakit jantung"
    bow = bagOfWord(judul)
    tf = termFrequency(bow)
    # print(len(bow), tf)

    idf = inverseDocumentFrequency(tf)
    tfidf = [calculateTfidf(i, idf) for i in tf]
    dftf = pd.DataFrame(tf)
    dftfidf = pd.DataFrame(tfidf)
    dfidf = pd.DataFrame([idf])
    print(dfidf)
    writer = pd.ExcelWriter("tfidf.xlsx", engine='xlsxwriter')
    dftf.to_excel(writer, sheet_name='TF')
    dfidf.to_excel(writer, sheet_name='IDF')
    dftfidf.to_excel(writer, sheet_name='TFIDF')
    writer.save()
    writer.close()

    CV = CountVectorizer()
    vectorizer = TfidfVectorizer(smooth_idf=True, use_idf=True)

    word_count_vec = CV.fit_transform(["deteksi penyakit tuberculosis","deteksi dini penyakit jantung"])
    tfidf = vectorizer.fit_transform(["deteksi penyakit tuberculosis","deteksi dini penyakit jantung"])
    query_vec = vectorizer.transform([query])
    results = cosine_similarity(tfidf, query_vec).reshape((-1,))
    print(vectorizer.idf_, vectorizer.get_feature_names_out())
    print(results)
    # print(tfidf)
    # print(bagOfWord(judul))