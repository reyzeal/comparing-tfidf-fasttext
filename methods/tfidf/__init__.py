import math
from pprint import pprint
import pandas as pd


def bag_of_words(tokens, bow_arr):
    bow = dict.fromkeys(bow_arr, 0)
    for i in bow.keys():
        bow[i] = tokens.count(i)
    return bow


"""
    Inverse Data Frequency
    menghitung frequency dari kata
"""


def inverse_data_frequency(documents):
    idf = {}
    for doc in documents:
        for word, value in doc.items():
            if value > 0:
                idf[word] = 1 + idf[word] if word in idf else 1

    total = len(documents)
    for word, count in idf.items():
        idf[word] = math.log10(float(total) / count)
    return idf


"""
    Term Frequency
    menghitung frequency dari kata
"""


def term_frequency(word_dict, bow):
    tf_dict = {}
    for word, count in word_dict.items():
        tf_dict[word] = float(count) / len(bow)
    return tf_dict


def query_tfidf(query, model):
    import preprocessing
    bow = model['bow']
    [preprocessed, _] = preprocessing.preprocessing(query)
    tf = term_frequency(bag_of_words(preprocessed, bow_arr=bow), bow=bow)
    Q = tfidf(tf, model['idf'])
    return Q


def cosine_similarity(Q, Ds):
    result = [0] * len(Ds)
    for i in range(len(Ds)):
        dot_product_xy = 0
        abs_x = 0
        abs_y = 0
        for j in Q.keys():
            x = Q[j]
            y = Ds[i][j]
            dot_product_xy += (x * y)
            abs_x += x ** 2
            abs_y += y ** 2
        abs_x = math.sqrt(abs_x)
        abs_y = math.sqrt(abs_y)
        result[i] = dot_product_xy / (abs_x * abs_y)
    return result

def similarity(query, model):
    Q = query_tfidf(query, model)
    labels = model['labels']
    result = list(zip(labels, cosine_similarity(Q, model['tfidf'])))
    result = sorted(result, key=lambda x: x[1], reverse=True)
    return result

def load_saved(model):
    import pickle
    with open(model, 'rb') as f:
        x = pickle.load(f)
        return x


def tfidf(tf, idf):
    result = {}
    for word, value in tf.items():
        result[word] = value * idf[word]
    return result


if __name__ == '__main__':
    import preprocessing

    test = [
        "Saya menyukai cabai dan paprika",
        "Petani-petani cabai sedang kewalahan mencari pupuk",
        "Buruh tani beralih menjadi kuli bangunan di departemen pertanian",
        "PDAM adalah perusahaan BUMN"
    ]
    test2 = [
        "The cat sat on my face",
        "The dog sat on my bed",
    ]
    tf = []
    word_dictionaries = []
    list_wd = []
    for i in test:
        preprocessed, _ = preprocessing.preprocessing(i)
        word_dictionaries = set(word_dictionaries).union(preprocessed)
    for i in test:
        preprocessed, _ = preprocessing.preprocessing(i)
        list_wd.append(bag_of_words(preprocessed, word_dictionaries))
    print("words", word_dictionaries)
    frequency = pd.DataFrame(list_wd)
    print(frequency)
    for i in list_wd:
        tf.append(term_frequency(i, word_dictionaries))
    tf_dataframe = pd.DataFrame(tf)
    print("tf",tf_dataframe)
    idf = inverse_data_frequency(tf)
    idf_dataframe = pd.DataFrame([idf])
    print(idf_dataframe)
    print(idf)
    result = []
    for i in tf:
        result.append(tfidf(i, idf))
    dataframe = pd.DataFrame(result)
    print(dataframe)
    pprint(result)
