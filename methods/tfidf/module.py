import math
import pickle

import numpy as np
import numpy.linalg as LA
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import preprocessing
from database import retrieve, retrieveByIndex

cosine_function = lambda a, b: round(np.inner(a, b) / (LA.norm(a) * LA.norm(b)), 3)


def Generate(trainset):
    # CV = CountVectorizer(stop_words=stopwords)
    vectorizer = TfidfVectorizer(smooth_idf=True, use_idf=True)

    # word_count_vec = CV.fit_transform(trainset).toarray()
    # tfidf = tfidf_transformer.fit_transform(word_count_vec)

    tfidf = vectorizer.fit_transform(trainset)

    with open("tfidf_features.bin", "wb") as f:
        pickle.dump(vectorizer.get_feature_names_out(), f)
    with open("tfidf_vectorizer.bin", "wb") as f:
        pickle.dump(vectorizer, f)
    with open("tfidf_data.bin", "wb") as f:
        pickle.dump(tfidf, f)
    print("tf",tfidf)
    # print(tfidf)


def Testing(testset, page = 1, limit = 10, socketio=None):
    socketio.emit("pencarian", "Melakukan preprocessing keyword")
    p = preprocessing.preprocessing(testset)
    test = p[0]

    with open("tfidf_features.bin", "rb") as f:
        features = pickle.load(f)
    socketio.emit("pencarian", "Loading vectorizer")
    with open("tfidf_vectorizer.bin", "rb") as f:
        vectorizer = pickle.load(f)
    socketio.emit("pencarian", "Loading data tfidf")
    with open("tfidf_data.bin", "rb") as f2:
        tfidf = pickle.load(f2)
    socketio.emit("pencarian", "Transformasi vector query")
    query_vec = vectorizer.transform([" ".join(test)])
    print("q",query_vec)
    socketio.emit("pencarian", "Cosine similarity")
    results = cosine_similarity(tfidf, query_vec).reshape((-1,))
    # for vector in trainArray:
    #     print(vector)
    #     for testV in query_vec:
    #         print(testV)
    #         cosine = cosine_function(vector, testV)
    #         print(cosine)
    data = []
    socketio.emit("pencarian", "Melakukan proses ranking")
    for i in results.argsort()[-limit*page:(len(results)-(page-1)*limit)][::-1]:
        # print(int(i))
        # print(i, retrieveByIndex(int(i))['data']['title'])

        x = retrieveByIndex(int(i))
        x['confidence'] = results[i]
        data.append(x)
        # print(df.iloc[i, 0], "--", df.iloc[i, 1])
    socketio.emit("pencarian", None)
    return {
        'data': data,
        'page': page,
        'limit': limit,
        'total': math.ceil(len(results)/limit),
        'hasPrev': page > 1,
        'hasNext': page < math.ceil(len(results)/limit),
        'next': page+1 if page < math.ceil(len(results)/limit) else None,
        'prev': page-1 if page > 1 else None,
    }
    # print(result)
