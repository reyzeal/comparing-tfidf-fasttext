import math
import pickle

from preprocessing import preprocessing


def build_dataset(text, dataset_name):
    with open("%s.txt" % dataset_name, 'w') as f:
        f.write(text)


def build_docs_set(docset, docset_name):
    result = [[None, None]] * len(docset)
    for i in range(len(docset)):
        result[i] = docset[i]
    with open("%s.bin" % docset_name, 'wb') as f:
        pickle.dump(result, f)


def training(model_name, dataset, dim=100, ws=4):
    import fasttext
    model = fasttext.train_unsupervised(dataset, model='skipgram', dim=dim, epoch=250, loss='ns', ws=ws)
    model.save_model(model_name)
    return model


def vector_len(v):
    return math.sqrt(sum([x * x for x in v]))


def dot_product(v1, v2):
    return sum([x * y for (x, y) in zip(v1, v2)])


def cosine_similarity(v1, v2):
    return dot_product(v1, v2) / (vector_len(v1) * vector_len(v2))


def similarity(query, modelname, docset_name):
    from gensim.models import FastText
    model = FastText.load_fasttext_format(modelname)
    q, _ = preprocessing(query)
    with open("%s.bin" % docset_name, 'rb') as f:
        docset = pickle.load(f)
    result = []
    for [_id, preprocessed] in docset:
        result.append((_id, model.wv.n_similarity(q, preprocessed)))
    result = sorted(result, key=lambda x: x[1], reverse=True)
    return result


def most_similar(model, x, top=10):
    v1 = model.get_word_vector(x)
    all_word = []
    for word in model.words:
        if word != x:
            v2 = model.get_word_vector(word)
            all_word.append((cosine_similarity(v1, v2), word))
    all_word = sorted(all_word, key=lambda item: item[0], reverse=True)
    return all_word[:top]


def load_model(model):
    import fasttext
    return fasttext.load_model(model)
