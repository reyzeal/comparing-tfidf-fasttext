import json
from pprint import pprint

import pandas as pd
import pickle
from database import retrieve, update
from preprocessing import preprocessing
import _fasttext
import tfidf
import threading


def tfidf_generate(documents):
    tf = []
    word_dictionaries = []
    list_wd = []
    labels = []
    for i in documents:
        [_id, text] = i
        labels.append(_id)
        word_dictionaries = set(word_dictionaries).union(text)
    for i in documents:
        [_id, text] = i
        list_wd.append(tfidf.bag_of_words(text, word_dictionaries))
    # print("words", word_dictionaries)
    # frequency = pd.DataFrame(list_wd)
    # print(frequency)
    for i in list_wd:
        tf.append(tfidf.term_frequency(i, word_dictionaries))
    # tf_dataframe = pd.DataFrame(tf)
    # print(tf_dataframe)
    idf = tfidf.inverse_data_frequency(tf)
    # idf_dataframe = pd.DataFrame([idf])
    # print(idf_dataframe)
    # print(idf)
    result = []
    for i in tf:
        result.append(tfidf.tfidf(i, idf))
    return {
        'labels': labels,
        'bow': word_dictionaries,
        'tf': tf,
        'idf': idf,
        'tfidf': result
    }
    # dataframe = pd.DataFrame(result)
    # print(dataframe)
    # pprint(result)


result = []


def worker(f, doc, _id):
    global result
    # print('preprocessed', doc, 'preprocessed' not in doc)
    if 'preprocessed' not in doc or doc['preprocessed'] is None:
        r = f(doc['data']['title'])
        result[_id] = [doc['_id'], r]
        update(doc['_id'], {'preprocessed': {'result': r[0], 'verbose': r[1]}})
    else:
        r = doc['preprocessed']
        result[_id] = [doc['_id'], [r['result'], r['verbose']]]


def eprint_retrieve():
    global result
    print("retrieving from database")
    data = retrieve()
    print("done retrieving from database")
    text = ""
    print("preprocessing", len(data))
    result = [None] * len(data)

    for i in range(0, len(data), 10):
        threads = []

        for j in range(10):
            if i + j < len(data):
                print(i + j, data[i + j]['_id'])
                threads.append(
                    threading.Thread(target=worker,
                                     args=(preprocessing, data[i + j], i + j)))

        for j in threads:
            j.start()

        for j in threads:
            j.join()

    dataset = []
    # result = [
    #     (0, preprocessing("Saya menyukai cabai dan paprika")),
    #     (1, preprocessing("Petani-petani cabai sedang kewalahan mencari pupuk")),
    #     (2, preprocessing("Buruh tani beralih menjadi kuli bangunan di departemen pertanian")),
    #     (3, preprocessing("PDAM adalah perusahaan BUMN")),
    # ]
    for i in result:
        [_id, obj] = i
        [preprocessed, _] = obj
        # print(preprocessed)
        dataset.append((_id, preprocessed))
        text = text + "\n" + " ".join(preprocessed)
    print("building dataset")
    _fasttext.build_dataset(text, "dataset")
    _fasttext.build_docs_set(dataset, "docset")

    x = tfidf_generate(dataset)
    with open("tfidf.bin", 'wb') as f:
        pickle.dump(x, f)

    print("training")
    for dim in [100, 300, 500]:
        for ws in [3, 4, 5]:
            _fasttext.training("model.%dw%d.bin" % (dim, ws), "dataset.txt", dim=dim, ws=ws)


def testing2():
    tfidf_model = tfidf.load_saved("tfidf.bin")
    query = "media sosial tfidf"
    x = tfidf.similarity(query, tfidf_model)
    result = [[(retrieve(i[0])['preprocessed']['verbose']['casefolding'], i[1]) for i in x[:10]]]
    for dim in [100, 300, 500]:
        for ws in [3, 4, 5]:
            temp = _fasttext.similarity(query, "model.%dw%d.bin" % (dim, ws), "docset")
            result.append([(retrieve(i[0])['preprocessed']['verbose']['casefolding'], i[1]) for i in temp[:10]])

    d = pd.DataFrame(result)
    print(d)
    d.to_excel("compare.xlsx")


def testing():
    model100 = _fasttext.load_model("model.100.bin")
    model300 = _fasttext.load_model("model.300.bin")
    tfidf_model = tfidf.load_saved("tfidf.bin")
    query = "tfidf"
    x = tfidf.similarity(query, tfidf_model)
    result_x = [(retrieve(i[0])['data']['title'], i[1]) for i in x[:10]]

    y = _fasttext.similarity(query, model100, "docset")
    z = _fasttext.similarity(query, model300, "docset")
    result_y = [(retrieve(i[0])['data']['title'], i[1]) for i in y[:10]]
    result_z = [(retrieve(i[0])['data']['title'], i[1]) for i in z[:10]]
    print(result_x)
    print(result_y)
    print(result_z)

    # model2 = _fasttext.load_model("model.300.bin")
    # result = _fasttext.most_similar(model, "media", 10)
    # result2 = _fasttext.most_similar(model2, "media", 10)
    #
    # print(result)
    # print(result2)


if __name__ == '__main__':
    # eprint_retrieve()
    testing2()
